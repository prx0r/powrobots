"""Tests for POWRobots — persistence, entities, collectors."""

import hashlib
import json
import os
import sys
import sqlite3
import pytest
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from powrobots.shared.persist import (
    get_db, store_raw, store_acquisition, insert_source_record,
    log_run, upsert_organisation, upsert_robot_manufacturer,
    upsert_robot_model, upsert_component, insert_relation,
    check_source_rights
)
from powrobots.shared.db import SCHEMA, _enable_foreign_keys


@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / 'test.db'
    os.environ['POWROBOTS_DB'] = str(db_path)
    conn = sqlite3.connect(str(db_path))
    _enable_foreign_keys(conn)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    yield db_path
    os.environ.pop('POWROBOTS_DB', None)


# =============================================================================
# FOREIGN KEYS
# =============================================================================

class TestForeignKeys:
    def test_fk_enforced(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        _enable_foreign_keys(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO robot_model (model_id, manufacturer_id, canonical_name) "
                "VALUES ('test', 'nonexistent', 'Test')"
            )
        conn.close()


# =============================================================================
# PERSISTENCE
# =============================================================================

class TestPersistence:
    def test_raw_dedup(self, temp_db):
        content = b'test data'
        r1 = store_raw(content, 'test')
        r2 = store_raw(content, 'test')
        assert r1['sha256'] == r2['sha256']
        assert r1['inserted'] is True
        assert r2['inserted'] is False

    def test_raw_immutability(self, temp_db):
        content = b'immutable'
        r = store_raw(content, 'test')
        store_raw(b'changed', 'test')
        import gzip
        with gzip.open(r['path'], 'rb') as f:
            assert f.read() == content

    def test_source_record_versioning(self, temp_db):
        ir1 = insert_source_record('test', 'ds', 'n1', {'k': 'v1'}, 'h1', 'p')
        ir2 = insert_source_record('test', 'ds', 'n1', {'k': 'v2'}, 'h2', 'p')
        assert ir1['inserted'] is True
        assert ir2['inserted'] is True
        assert ':v' in ir2['record_id']

    def test_source_record_dedup(self, temp_db):
        ir1 = insert_source_record('test', 'ds', 'n1', {'k': 'v1'}, 'h1', 'p')
        ir2 = insert_source_record('test', 'ds', 'n1', {'k': 'v1'}, 'h2', 'p')
        assert ir1['inserted'] is True
        assert ir2['inserted'] is False

    def test_acquisition_appends(self, temp_db):
        r = store_raw(b'test', 'test')
        store_acquisition('test', 'ds', 'http://example.com', 200, r['sha256'])
        store_acquisition('test', 'ds', 'http://example.com', 200, r['sha256'])
        conn = sqlite3.connect(str(temp_db))
        count = conn.execute('SELECT COUNT(*) FROM raw_acquisition').fetchone()[0]
        assert count == 2
        conn.close()


# =============================================================================
# ENTITY GRAPH
# =============================================================================

class TestEntityGraph:
    def test_organisation_upsert(self, temp_db):
        upsert_organisation('OC123456', 'Test Company Ltd', company_number='OC123456')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT canonical_name FROM organisation WHERE org_id="OC123456"').fetchone()
        assert row[0] == 'Test Company Ltd'
        conn.close()

    def test_robot_manufacturer_upsert(self, temp_db):
        upsert_robot_manufacturer('fanuc', 'FANUC', country_code='JP')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT canonical_name FROM robot_manufacturer WHERE manufacturer_id="fanuc"').fetchone()
        assert row[0] == 'FANUC'
        conn.close()

    def test_robot_model_upsert(self, temp_db):
        upsert_robot_manufacturer('fanuc', 'FANUC')
        upsert_robot_model('fanuc-m10ia', 'fanuc', 'FANUC M-10iA',
                            robot_type='industrial_arm', axes=6, payload_kg=12,
                            reach_mm=1441)
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute(
            'SELECT canonical_name, axes, payload_kg FROM robot_model WHERE model_id="fanuc-m10ia"'
        ).fetchone()
        assert row[0] == 'FANUC M-10iA'
        assert row[1] == 6
        assert row[2] == 12.0
        conn.close()

    def test_component_upsert(self, temp_db):
        upsert_component('servo-xm430', 'DYNAMIXEL XM430-W350', mpn='XM430-W350')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT canonical_name FROM component WHERE component_id="servo-xm430"').fetchone()
        assert row[0] == 'DYNAMIXEL XM430-W350'
        conn.close()

    def test_relation(self, temp_db):
        upsert_robot_manufacturer('fanuc', 'FANUC')
        upsert_robot_model('fanuc-m10ia', 'fanuc', 'FANUC M-10iA')
        upsert_component('servo-m10ia', 'FANUC Servo Motor')
        rid = insert_relation('fanuc-m10ia', 'servo-m10ia', 'USES_COMPONENT',
                               confidence='declared')
        assert rid is not None
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT relation_type FROM product_relation WHERE relation_id=?', (rid,)).fetchone()
        assert row[0] == 'USES_COMPONENT'
        conn.close()


# =============================================================================
# ROBOT ONTOLOGY
# =============================================================================

class TestRobotOntology:
    def test_robot_types(self, temp_db):
        from powrobots.core.enums import RobotType
        assert RobotType.INDUSTRIAL_ARM.value == 'industrial_arm'
        assert RobotType.HUMANOID.value == 'humanoid'

    def test_model_with_specs(self, temp_db):
        upsert_robot_manufacturer('ur', 'Universal Robots')
        upsert_robot_model('ur5e', 'ur', 'UR5e',
                            robot_type='cobot', axes=6, payload_kg=5.0,
                            reach_mm=850.0, repeatability_mm=0.1)
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT payload_kg, reach_mm, repeatability_mm FROM robot_model WHERE model_id="ur5e"').fetchone()
        assert row[0] == 5.0
        assert row[1] == 850.0
        assert row[2] == 0.1
        conn.close()


# =============================================================================
# SOURCE RIGHTS
# =============================================================================

class TestRights:
    def test_blocked_source(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        conn.execute("INSERT INTO source_rights (source_id, status) VALUES ('blocked', 'blocked')")
        conn.commit()
        conn.close()
        rights = check_source_rights('blocked')
        assert rights['allowed'] is False

    def test_open_source(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        conn.execute("INSERT INTO source_rights (source_id, status) VALUES ('open', 'open')")
        conn.commit()
        conn.close()
        rights = check_source_rights('open')
        assert rights['allowed'] is True


# =============================================================================
# SEEDS
# =============================================================================

class TestSeeds:
    def test_manufacturers_seed_loadable(self):
        import yaml
        seed_path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'manufacturers.yml')
        with open(seed_path) as f:
            data = yaml.safe_load(f)
        assert len(data) >= 20
        assert all('id' in m and 'name' in m for m in data)

    def test_hs_codes_seed_loadable(self):
        import yaml
        seed_path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'hs_codes.yml')
        with open(seed_path) as f:
            data = yaml.safe_load(f)
        assert len(data) >= 10
        assert data[0]['code'] == '847950'


# =============================================================================
# COLLECTOR BASE
# =============================================================================

class TestBaseCollector:
    def test_rights_blocked(self, temp_db):
        from powrobots.collectors.base import BaseCollector, CollectorResult
        class Blocked(BaseCollector):
            SOURCE_ID = 'blocked_c'
            DATASET = 'test'
            PARSER_ID = 'test'
            def fetch(self): return b'data'
            def parse(self, raw_content, raw_hash, result): pass
        conn = sqlite3.connect(str(temp_db))
        conn.execute("INSERT INTO source_rights (source_id, status) VALUES ('blocked_c', 'blocked')")
        conn.commit()
        conn.close()
        result = Blocked().run()
        assert 'rights_blocked' in result.errors


# =============================================================================
# DAEMON
# =============================================================================

class TestDaemon:
    def test_daemon_registry(self):
        # Verify collector classes are importable
        from powrobots.collectors.companies_house import CompaniesHouseCollector
        from powrobots.collectors.ukri_gtr import UkriGtrCollector
        from powrobots.collectors.mouser import MouserCollector
        assert CompaniesHouseCollector.SOURCE_ID == 'companies_house'
        assert UkriGtrCollector.SOURCE_ID == 'ukri_gtr'
        assert MouserCollector.SOURCE_ID == 'mouser'


# =============================================================================
# SCHEMA INTEGRITY
# =============================================================================

class TestSchema:
    def test_all_tables_created(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'schema_version'"
        ).fetchall()]
        expected = [
            'raw_blob', 'raw_acquisition', 'source_record', 'source_cursor',
            'collector_run', 'source_health', 'source_rights',
            'organisation', 'robot_manufacturer', 'robot_family', 'robot_model',
            'component_manufacturer', 'component', 'component_category', 'distributor',
            'product_relation', 'market_listing', 'market_observation',
            'component_market_observation', 'uk_trade_record',
            'procurement_notice', 'grant_project',
            'apprenticeship_listing', 'job_listing',
            'safety_notice', 'deployment_evidence',
            'company_filing', 'change_event', 'robot_description',
        ]
        for t in expected:
            assert t in tables, f'Missing table: {t}'
        conn.close()
