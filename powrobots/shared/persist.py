"""Persistence — shared functions for all collectors."""

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from powrobots.shared.db import get_db, _enable_foreign_keys


def store_raw(content: bytes, source_id: str, content_type: str = 'application/octet-stream'):
    sha256 = hashlib.sha256(content).hexdigest()
    db_path = __import__('powrobots.shared.db', fromlist=['get_db_path']).get_db_path()
    raw_dir = db_path.parent / 'raw' / source_id
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f'{sha256}.gz'
    inserted = not raw_path.exists()
    if inserted:
        import gzip
        with gzip.open(raw_path, 'wb') as f:
            f.write(content)
    conn = get_db()
    cursor = conn.execute(
        "INSERT OR IGNORE INTO raw_blob (sha256, source_id, content_type, content_length, storage_path) "
        "VALUES (?, ?, ?, ?, ?)",
        (sha256, source_id, content_type, len(content), str(raw_path))
    )
    if cursor.rowcount == 0:
        inserted = False
    conn.commit()
    conn.close()
    return {'sha256': sha256, 'inserted': inserted, 'path': str(raw_path)}


def store_acquisition(source_id: str, dataset: str, url: str, http_status: int,
                      sha256: str, content_type: str = '', content_length: int = 0):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO raw_acquisition "
        "(source_id, dataset, retrieved_at, request_url, http_status, content_type, content_length, sha256) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (source_id, dataset, datetime.now(timezone.utc).isoformat(),
         url, http_status, content_type, content_length, sha256)
    )
    acq_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return acq_id


def insert_source_record(source_id: str, dataset: str, native_id: str,
                          normalized: dict, raw_hash: str, parser_id: str,
                          parser_version: str = '1.0.0', acquisition_id: int = None):
    record_id = f'{source_id}:{native_id}'
    payload_hash = hashlib.sha256(
        json.dumps(normalized, sort_keys=True, default=str).encode()
    ).hexdigest()
    conn = get_db()
    existing = conn.execute(
        "SELECT source_record_id, payload_hash FROM source_record "
        "WHERE source_record_id = ? OR source_record_id LIKE ? "
        "ORDER BY retrieved_at DESC LIMIT 1",
        (record_id, f'{record_id}:v%')
    ).fetchone()
    if existing:
        if existing[1] == payload_hash:
            conn.close()
            return {'inserted': False, 'record_id': existing[0], 'duplicate_of': existing[0]}
        version_id = f'{record_id}:v{payload_hash[:12]}'
        try:
            conn.execute(
                "INSERT INTO source_record "
                "(source_record_id, source_id, dataset, source_native_id, retrieved_at, "
                "normalized_json, payload_hash, raw_payload_hash, acquisition_id, parser_id, parser_version) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (version_id, source_id, dataset, native_id,
                 datetime.now(timezone.utc).isoformat(),
                 json.dumps(normalized, default=str), payload_hash,
                 raw_hash, acquisition_id, parser_id, parser_version)
            )
            conn.commit()
            conn.close()
            return {'inserted': True, 'record_id': version_id, 'duplicate_of': record_id}
        except sqlite3.IntegrityError:
            conn.close()
            return {'inserted': False, 'record_id': version_id, 'duplicate_of': record_id}
    try:
        conn.execute(
            "INSERT INTO source_record "
            "(source_record_id, source_id, dataset, source_native_id, retrieved_at, "
            "normalized_json, payload_hash, raw_payload_hash, acquisition_id, parser_id, parser_version) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (record_id, source_id, dataset, native_id,
             datetime.now(timezone.utc).isoformat(),
             json.dumps(normalized, default=str), payload_hash,
             raw_hash, acquisition_id, parser_id, parser_version)
        )
        conn.commit()
        conn.close()
        return {'inserted': True, 'record_id': record_id}
    except sqlite3.IntegrityError:
        conn.close()
        return {'inserted': False, 'record_id': record_id, 'duplicate_of': record_id}


def log_run(source_id: str, status: str, raw_fetched: int = 0, raw_new: int = 0,
            records_new: int = 0, records_unchanged: int = 0, records_changed: int = 0,
            records_invalid: int = 0, error: str = None,
            started_at: str = '', finished_at: str = '',
            collector_sha: str = '', cursor_before: str = '', cursor_after: str = '',
            validation_passed: int = 1, schema_version: str = ''):
    conn = get_db()
    duration = None
    if started_at and finished_at:
        try:
            from datetime import datetime as dt
            s = dt.fromisoformat(started_at.replace('Z', '+00:00'))
            f = dt.fromisoformat(finished_at.replace('Z', '+00:00'))
            duration = (f - s).total_seconds()
        except (ValueError, TypeError):
            pass

    conn.execute(
        "INSERT INTO collector_run "
        "(source_id, started_at, finished_at, status, raw_fetched, raw_new, "
        "source_records_new, source_records_updated, source_records_invalid, "
        "error, duration_seconds, collector_sha, cursor_before, cursor_after, "
        "validation_passed, schema_version) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (source_id, started_at or datetime.now(timezone.utc).isoformat(),
         finished_at or datetime.now(timezone.utc).isoformat(),
         status, raw_fetched, raw_new, records_new, records_changed, records_invalid,
         error, duration, collector_sha or None, cursor_before or None,
         cursor_after or None, validation_passed, schema_version or None)
    )
    conn.commit()
    run_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()

    # Update source_health after each run
    try:
        compute_source_health(source_id)
    except Exception:
        pass

    return run_id


def compute_source_health(source_id: str):
    """Compute and write source_health from latest collector_run.

    Called automatically after each log_run().
    """
    conn = get_db()
    row = conn.execute(
        "SELECT started_at, finished_at, status, error, "
        "source_records_new, source_records_updated, source_records_invalid "
        "FROM collector_run WHERE source_id = ? ORDER BY run_id DESC LIMIT 1",
        (source_id,)
    ).fetchone()

    if not row:
        conn.close()
        return

    started_at, finished_at, status, error, new, updated, invalid = row

    # Determine health status
    if status == 'ok':
        health_status = 'healthy'
        health_reason = None
    elif status == 'error':
        health_status = 'failed'
        health_reason = error
    elif status == 'blocked':
        health_status = 'blocked'
        health_reason = error or 'rights_blocked'
    else:
        health_status = 'unknown'
        health_reason = status

    # Check if health record exists
    existing = conn.execute(
        "SELECT health_id FROM source_health WHERE source_id = ?",
        (source_id,)
    ).fetchone()

    now = datetime.now(timezone.utc).isoformat()

    if existing:
        # Update
        is_success = status == 'ok'
        conn.execute(
            "UPDATE source_health SET "
            "last_attempt = ?, last_success = CASE WHEN ? THEN ? ELSE last_success END, "
            "last_error = CASE WHEN ? THEN ? ELSE last_error END, "
            "records_new = ?, records_changed = ?, records_invalid = ?, "
            "status = ?, status_reason = ?, computed_at = ? "
            "WHERE source_id = ?",
            (started_at, is_success, finished_at,
             not is_success, error,
             new or 0, updated or 0, invalid or 0,
             health_status, health_reason, now, source_id)
        )
    else:
        # Insert
        conn.execute(
            "INSERT INTO source_health "
            "(source_id, last_attempt, last_success, last_error, "
            "records_new, records_changed, records_invalid, "
            "status, status_reason, computed_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (source_id, started_at,
             finished_at if status == 'ok' else None,
             error if status != 'ok' else None,
             new or 0, updated or 0, invalid or 0,
             health_status, health_reason, now)
        )

    conn.commit()
    conn.close()


def upsert_organisation(org_id: str, canonical_name: str, company_number: str = '',
                         sic_code: str = '', country_code: str = 'GB', region: str = '',
                         website: str = '', org_type: str = '', aliases: list = None):
    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO organisation (org_id, canonical_name, aliases_json, company_number, "
        "sic_code, country_code, region, website, org_type, first_seen_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(org_id) DO UPDATE SET "
        "canonical_name=excluded.canonical_name, last_seen_at=excluded.last_seen_at",
        (org_id, canonical_name, json.dumps(aliases or []), company_number,
         sic_code, country_code, region, website, org_type, now, now)
    )
    conn.commit()
    conn.close()


def upsert_robot_manufacturer(manufacturer_id: str, canonical_name: str,
                               org_id: str = None, country_code: str = '', website: str = '',
                               uk_distributor: str = '', aliases: list = None):
    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO robot_manufacturer (manufacturer_id, org_id, canonical_name, aliases_json, "
        "country_code, website, uk_distributor, first_seen_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(manufacturer_id) DO UPDATE SET "
        "canonical_name=excluded.canonical_name, last_seen_at=excluded.last_seen_at",
        (manufacturer_id, org_id, canonical_name, json.dumps(aliases or []),
         country_code, website, uk_distributor, now, now)
    )
    conn.commit()
    conn.close()


def upsert_robot_model(model_id: str, manufacturer_id: str, canonical_name: str,
                        family_id: str = None, robot_type: str = '', axes: int = None,
                        payload_kg: float = None, reach_mm: float = None,
                        mass_kg: float = None, repeatability_mm: float = None,
                        controller: str = '', status: str = 'active',
                        aliases: list = None):
    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO robot_model (model_id, manufacturer_id, family_id, canonical_name, aliases_json, "
        "robot_type, axes, payload_kg, reach_mm, mass_kg, repeatability_mm, controller, "
        "status, first_seen_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(model_id) DO UPDATE SET "
        "canonical_name=excluded.canonical_name, last_seen_at=excluded.last_seen_at",
        (model_id, manufacturer_id, family_id, canonical_name, json.dumps(aliases or []),
         robot_type, axes, payload_kg, reach_mm, mass_kg, repeatability_mm,
         controller, status, now, now)
    )
    conn.commit()
    conn.close()


def upsert_component(component_id: str, canonical_name: str, manufacturer_id: str = None,
                      mpn: str = '', category: str = '', description: str = ''):
    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO component (component_id, manufacturer_id, canonical_name, mpn, "
        "category, description, first_seen_at, last_seen_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
        "ON CONFLICT(component_id) DO UPDATE SET "
        "canonical_name=excluded.canonical_name, last_seen_at=excluded.last_seen_at",
        (component_id, manufacturer_id, canonical_name, mpn, category, description, now, now)
    )
    conn.commit()
    conn.close()


def insert_relation(src_id: str, dst_id: str, relation_type: str,
                     confidence: str = 'declared', evidence_json: str = '',
                     source_record_id: str = ''):
    raw = f'{src_id}:{dst_id}:{relation_type}'
    relation_id = hashlib.sha256(raw.encode()).hexdigest()[:16]
    conn = get_db()
    now = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute(
            "INSERT INTO product_relation (relation_id, src_entity_id, dst_entity_id, "
            "relation_type, confidence, evidence_json, source_record_id, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (relation_id, src_id, dst_id, relation_type, confidence,
             evidence_json, source_record_id, now)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return relation_id


def check_source_rights(source_id: str) -> dict:
    conn = get_db()
    row = conn.execute("SELECT status FROM source_rights WHERE source_id=?", (source_id,)).fetchone()
    conn.close()
    if row is None:
        return {'allowed': False, 'status': 'not_registered'}
    if row[0] in ('open', 'approved'):
        return {'allowed': True, 'status': row[0]}
    return {'allowed': False, 'status': row[0]}
