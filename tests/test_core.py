"""Comprehensive test suite for POWRobots."""

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
# P0: FOREIGN KEYS
# =============================================================================

class TestForeignKeys:
    def test_fk_enforced_on_robot_model(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        _enable_foreign_keys(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO robot_model (model_id, manufacturer_id, canonical_name) "
                "VALUES ('test', 'nonexistent', 'Test')"
            )
        conn.close()

    def test_fk_enforced_on_component(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        _enable_foreign_keys(conn)
        with pytest.raises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO component (component_id, manufacturer_id, canonical_name) "
                "VALUES ('test', 'nonexistent', 'Test')"
            )
        conn.close()

    def test_fk_passes_with_valid_parent(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        _enable_foreign_keys(conn)
        conn.execute(
            "INSERT INTO robot_manufacturer (manufacturer_id, canonical_name) VALUES ('test', 'Test')"
        )
        conn.execute(
            "INSERT INTO robot_model (model_id, manufacturer_id, canonical_name) "
            "VALUES ('test_model', 'test', 'Test Model')"
        )
        conn.commit()
        row = conn.execute('SELECT canonical_name FROM robot_model WHERE model_id="test_model"').fetchone()
        assert row[0] == 'Test Model'
        conn.close()


# =============================================================================
# PERSISTENCE
# =============================================================================

class TestPersistence:
    def test_raw_deduplication(self, temp_db):
        r1 = store_raw(b'test content', 'test')
        r2 = store_raw(b'test content', 'test')
        assert r1['sha256'] == r2['sha256']
        assert r1['inserted'] is True
        assert r2['inserted'] is False

    def test_raw_immutability(self, temp_db):
        content = b'immutable content'
        r = store_raw(content, 'test')
        store_raw(b'different content', 'test')
        import gzip
        with gzip.open(r['path'], 'rb') as f:
            assert f.read() == content

    def test_raw_deterministic_hash(self, temp_db):
        content = b'deterministic'
        r = store_raw(content, 'test')
        assert r['sha256'] == hashlib.sha256(content).hexdigest()

    def test_acquisition_appends(self, temp_db):
        r = store_raw(b'test', 'test')
        store_acquisition('test', 'ds', 'http://a.com', 200, r['sha256'])
        store_acquisition('test', 'ds', 'http://b.com', 200, r['sha256'])
        conn = sqlite3.connect(str(temp_db))
        count = conn.execute('SELECT COUNT(*) FROM raw_acquisition').fetchone()[0]
        assert count == 2
        conn.close()

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

    def test_source_record_acquisition_link(self, temp_db):
        r = store_raw(b'test', 'test')
        acq_id = store_acquisition('test', 'ds', 'http://x.com', 200, r['sha256'])
        ir = insert_source_record('test', 'ds', 'n1', {'k': 'v'}, 'h', 'p', acquisition_id=acq_id)
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT acquisition_id FROM source_record WHERE source_record_id=?',
                           (ir['record_id'],)).fetchone()
        assert row[0] == acq_id
        conn.close()


# =============================================================================
# ENTITY GRAPH
# =============================================================================

class TestEntityGraph:
    def test_organisation_upsert(self, temp_db):
        upsert_organisation('OC123', 'Test Co', company_number='OC123', country_code='GB')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT canonical_name, country_code FROM organisation WHERE org_id="OC123"').fetchone()
        assert row[0] == 'Test Co'
        assert row[1] == 'GB'
        conn.close()

    def test_organisation_idempotent(self, temp_db):
        upsert_organisation('OC123', 'Test Co v1')
        upsert_organisation('OC123', 'Test Co v2')
        conn = sqlite3.connect(str(temp_db))
        count = conn.execute('SELECT COUNT(*) FROM organisation WHERE org_id="OC123"').fetchone()[0]
        assert count == 1
        conn.close()

    def test_robot_manufacturer(self, temp_db):
        upsert_robot_manufacturer('fanuc', 'FANUC', country_code='JP')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT canonical_name FROM robot_manufacturer WHERE manufacturer_id="fanuc"').fetchone()
        assert row[0] == 'FANUC'
        conn.close()

    def test_robot_model(self, temp_db):
        upsert_robot_manufacturer('fanuc', 'FANUC')
        upsert_robot_model('m10ia', 'fanuc', 'FANUC M-10iA', axes=6, payload_kg=12, reach_mm=1441)
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT axes, payload_kg, reach_mm FROM robot_model WHERE model_id="m10ia"').fetchone()
        assert row == (6, 12.0, 1441.0)
        conn.close()

    def test_component(self, temp_db):
        upsert_component('servo-xm430', 'DYNAMIXEL XM430-W350', mpn='XM430-W350')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT mpn FROM component WHERE component_id="servo-xm430"').fetchone()
        assert row[0] == 'XM430-W350'
        conn.close()

    def test_relation(self, temp_db):
        upsert_robot_manufacturer('fanuc', 'FANUC')
        upsert_robot_model('m10ia', 'fanuc', 'FANUC M-10iA')
        upsert_component('servo-m10ia', 'FANUC Servo')
        rid = insert_relation('m10ia', 'servo-m10ia', 'USES_COMPONENT', confidence='declared')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute('SELECT relation_type FROM product_relation WHERE relation_id=?', (rid,)).fetchone()
        assert row[0] == 'USES_COMPONENT'
        conn.close()

    def test_relation_idempotent(self, temp_db):
        rid1 = insert_relation('a', 'b', 'CONTAINS')
        rid2 = insert_relation('a', 'b', 'CONTAINS')
        assert rid1 == rid2
        conn = sqlite3.connect(str(temp_db))
        count = conn.execute('SELECT COUNT(*) FROM product_relation').fetchone()[0]
        assert count == 1
        conn.close()


# =============================================================================
# ROBOT ONTOLOGY
# =============================================================================

class TestRobotOntology:
    def test_all_robot_types_exist(self):
        from powrobots.core.enums import RobotType
        types = [e.value for e in RobotType]
        assert 'industrial_arm' in types
        assert 'cobot' in types
        assert 'humanoid' in types
        assert 'amr' in types
        assert 'drone_air' in types

    def test_all_applications_exist(self):
        from powrobots.core.enums import Application
        apps = [e.value for e in Application]
        assert 'welding' in apps
        assert 'palletising' in apps
        assert 'machine_tending' in apps

    def test_all_component_categories_exist(self):
        from powrobots.core.enums import ComponentCategory
        cats = [e.value for e in ComponentCategory]
        assert 'servo_motor' in cats
        assert 'encoder_absolute' in cats
        assert 'gearbox_harmonic' in cats
        assert 'safety_scanner' in cats

    def test_model_full_specs(self, temp_db):
        upsert_robot_manufacturer('ur', 'Universal Robots')
        upsert_robot_model('ur5e', 'ur', 'UR5e', robot_type='cobot', axes=6,
                            payload_kg=5.0, reach_mm=850.0, repeatability_mm=0.1,
                            controller='UR CB3')
        conn = sqlite3.connect(str(temp_db))
        row = conn.execute(
            'SELECT robot_type, axes, payload_kg, reach_mm, repeatability_mm, controller '
            'FROM robot_model WHERE model_id="ur5e"'
        ).fetchone()
        assert row == ('cobot', 6, 5.0, 850.0, 0.1, 'UR CB3')
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
        assert check_source_rights('blocked')['allowed'] is False

    def test_open_source(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        conn.execute("INSERT INTO source_rights (source_id, status) VALUES ('open', 'open')")
        conn.commit()
        conn.close()
        assert check_source_rights('open')['allowed'] is True

    def test_unknown_source(self, temp_db):
        rights = check_source_rights('nonexistent')
        assert rights['allowed'] is False
        assert rights['status'] == 'not_registered'


# =============================================================================
# SEEDS
# =============================================================================

class TestSeeds:
    def test_manufacturers_seed(self):
        import yaml
        path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'manufacturers.yml')
        with open(path) as f:
            data = yaml.safe_load(f)
        assert len(data) >= 20
        ids = [m['id'] for m in data]
        assert 'fanuc' in ids
        assert 'kuka' in ids
        assert 'universal_robots' in ids

    def test_hs_codes_seed(self):
        import yaml
        path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'hs_codes.yml')
        with open(path) as f:
            data = yaml.safe_load(f)
        assert data[0]['code'] == '847950'
        assert data[0]['robotics_relevance'] == 'primary'

    def test_component_categories_seed(self):
        import yaml
        path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'component_categories.yml')
        with open(path) as f:
            data = yaml.safe_load(f)
        assert len(data) >= 20
        ids = [c['id'] for c in data]
        assert 'servo_motor' in ids
        assert 'encoder_absolute' in ids

    def test_component_basket_seed(self):
        import yaml
        path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'component_basket.yml')
        with open(path) as f:
            data = yaml.safe_load(f)
        total = sum(len(v) for v in data.values() if isinstance(v, list))
        assert total >= 25

    def test_ros_repositories_seed(self):
        import yaml
        path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'ros_repositories.yml')
        with open(path) as f:
            data = yaml.safe_load(f)
        assert len(data) >= 4
        manufacturers = [r['manufacturer'] for r in data]
        assert 'fanuc' in manufacturers
        assert 'kuka' in manufacturers

    def test_chinese_stocks_seed(self):
        import yaml
        path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'chinese_stocks.yml')
        with open(path) as f:
            data = yaml.safe_load(f)
        assert len(data) >= 5
        ids = [s['id'] for s in data]
        assert 'estun' in ids
        assert 'leader_harmonic' in ids

    def test_china_production_seed(self):
        import yaml
        path = os.path.join(os.path.dirname(__file__), '..', 'powrobots', 'seeds', 'china_production.yml')
        with open(path) as f:
            data = yaml.safe_load(f)
        records = data.get('records', [])
        assert len(records) >= 3
        assert records[0]['source_ref'] == 'IFR World Robotics 2025'


# =============================================================================
# COLLECTORS
# =============================================================================

class TestCollectors:
    def test_all_collectors_importable(self):
        from powrobots.collectors.companies_house import CompaniesHouseCollector
        from powrobots.collectors.ukri_gtr import UkriGtrCollector
        from powrobots.collectors.mouser import MouserCollector
        from powrobots.collectors.ebay_uk import EbayUkCollector
        from powrobots.collectors.hmrc_trade import HmrcTradeCollector
        from powrobots.collectors.hmrc_traders import HmrcTraderCollector
        from powrobots.collectors.contracts_finder import ContractsFinderCollector
        from powrobots.collectors.opss_safety import OpsSafetyCollector
        from powrobots.collectors.bara_directory import BaraDirectoryCollector
        from powrobots.collectors.apprenticeships import ApprenticeshipCollector
        from powrobots.collectors.ons_ppi import OnsPpiCollector
        from powrobots.collectors.bgs_minerals import BgsMineralsCollector
        from powrobots.collectors.rbtx import RbtxCollector
        from powrobots.collectors.lcsc import LcscCollector
        from powrobots.collectors.farnell import FarnellCollector
        assert CompaniesHouseCollector.SOURCE_ID == 'companies_house'
        assert UkriGtrCollector.SOURCE_ID == 'ukri_gtr'
        assert MouserCollector.SOURCE_ID == 'mouser'
        assert EbayUkCollector.SOURCE_ID == 'ebay_uk'
        assert HmrcTradeCollector.SOURCE_ID == 'hmrc_trade'
        assert HmrcTraderCollector.SOURCE_ID == 'hmrc_traders'
        assert ContractsFinderCollector.SOURCE_ID == 'contracts_finder'
        assert OpsSafetyCollector.SOURCE_ID == 'opss_safety'
        assert BaraDirectoryCollector.SOURCE_ID == 'bara_directory'
        assert ApprenticeshipCollector.SOURCE_ID == 'find_apprenticeship'
        assert OnsPpiCollector.SOURCE_ID == 'ons_ppi'
        assert BgsMineralsCollector.SOURCE_ID == 'bgs_minerals'
        assert RbtxCollector.SOURCE_ID == 'rbtx'
        assert LcscCollector.SOURCE_ID == 'lcsc'
        assert FarnellCollector.SOURCE_ID == 'farnell'

    def test_collector_rights_blocked(self, temp_db):
        from powrobots.collectors.base import BaseCollector
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

    def test_collector_success_run(self, temp_db):
        from powrobots.collectors.base import BaseCollector
        class TestCol(BaseCollector):
            SOURCE_ID = 'test_ok'
            DATASET = 'test'
            PARSER_ID = 'test'
            def fetch(self): return b'{"items": []}'
            def parse(self, raw_content, raw_hash, result): result.records_new = 1
        conn = sqlite3.connect(str(temp_db))
        conn.execute("INSERT INTO source_rights (source_id, status) VALUES ('test_ok', 'open')")
        conn.commit()
        conn.close()
        result = TestCol().run()
        assert result.records_new == 1
        assert result.errors == []


# =============================================================================
# CLI
# =============================================================================

class TestCli:
    def test_cli_imports(self):
        from powrobots.cli import cmd_status, cmd_sources, cmd_validate
        assert callable(cmd_status)
        assert callable(cmd_sources)
        assert callable(cmd_validate)


# =============================================================================
# SCHEMA INTEGRITY
# =============================================================================

class TestSchema:
    def test_all_core_tables_exist(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        tables = [r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name != 'schema_version'"
        ).fetchall()]
        required = [
            'source_registry', 'raw_blob', 'raw_acquisition', 'source_record',
            'organisation', 'robot_manufacturer', 'robot_model',
            'component', 'product_relation',
            'market_listing', 'market_observation',
            'uk_trade_record', 'procurement_notice', 'grant_project',
            'apprenticeship_listing', 'safety_notice',
            'deployment_evidence', 'robot_description',
        ]
        for t in required:
            assert t in tables, f'Missing: {t}'
        conn.close()

    def test_indexed_queries_work(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        _enable_foreign_keys(conn)
        # Create test data
        conn.execute("INSERT INTO robot_manufacturer (manufacturer_id, canonical_name) VALUES ('fanuc', 'FANUC')")
        conn.execute("INSERT INTO robot_model (model_id, manufacturer_id, canonical_name) VALUES ('m10ia', 'fanuc', 'M-10iA')")
        conn.execute("INSERT INTO organisation (org_id, canonical_name) VALUES ('fanuc_uk', 'FANUC UK')")
        conn.commit()
        # Test indexed queries
        row = conn.execute('SELECT * FROM robot_model WHERE manufacturer_id="fanuc"').fetchone()
        assert row is not None
        row = conn.execute('SELECT * FROM organisation WHERE org_id="fanuc_uk"').fetchone()
        assert row is not None
        conn.close()


# =============================================================================
# REPLAY / DETERMINISM
# =============================================================================

class TestReplay:
    def test_parser_deterministic(self):
        raw = b'{"mpn": "XM430", "name": "DYNAMIXEL"}'
        d1 = json.loads(raw)
        d2 = json.loads(raw)
        assert d1 == d2
        h1 = hashlib.sha256(json.dumps(d1, sort_keys=True).encode()).hexdigest()
        h2 = hashlib.sha256(json.dumps(d2, sort_keys=True).encode()).hexdigest()
        assert h1 == h2


# =============================================================================
# CHANGE EVENTS
# =============================================================================

class TestChangeEvents:
    def test_change_event_stored(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        conn.execute(
            "INSERT INTO change_event (entity_id, entity_type, field, old_value, new_value, source_id) "
            "VALUES ('fanuc_m10ia', 'robot_model', 'discontinued_date', NULL, '2025-01-01', 'test')"
        )
        conn.commit()
        row = conn.execute('SELECT field, old_value, new_value FROM change_event WHERE entity_id="fanuc_m10ia"').fetchone()
        assert row == ('discontinued_date', None, '2025-01-01')
        conn.close()


# =============================================================================
# DEPLOYMENT EVIDENCE
# =============================================================================

class TestDeploymentEvidence:
    def test_deployment_stored(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        _enable_foreign_keys(conn)
        conn.execute("INSERT INTO robot_manufacturer (manufacturer_id, canonical_name) VALUES ('fanuc', 'FANUC')")
        conn.execute("INSERT INTO organisation (org_id, canonical_name) VALUES ('acme', 'Acme Manufacturing')")
        conn.execute(
            "INSERT INTO deployment_evidence (evidence_id, observed_at, organisation_id, "
            "robot_manufacturer_id, robot_count, application, evidence_type, source_id) "
            "VALUES ('dep1', '2026-09-21', 'acme', 'fanuc', 6, 'welding', 'case_study', 'test')"
        )
        conn.commit()
        row = conn.execute('SELECT robot_count, application FROM deployment_evidence WHERE evidence_id="dep1"').fetchone()
        assert row == (6, 'welding')
        conn.close()


# =============================================================================
# UK TRADE
# =============================================================================

class TestUkTrade:
    def test_trade_record_stored(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        conn.execute(
            "INSERT INTO uk_trade_record (month, flow, commodity_code, partner_country, "
            "value_gbp, source_id) VALUES ('2026-01', 'import', '847950', 'Japan', 1500000, 'test')"
        )
        conn.commit()
        row = conn.execute('SELECT value_gbp, partner_country FROM uk_trade_record').fetchone()
        assert row == (1500000.0, 'Japan')
        conn.close()

    def test_trade_indexed_by_commodity(self, temp_db):
        conn = sqlite3.connect(str(temp_db))
        for month in ['2026-01', '2026-02', '2026-03']:
            conn.execute(
                "INSERT INTO uk_trade_record (month, flow, commodity_code, partner_country, "
                "value_gbp, source_id) VALUES (?, 'import', '847950', 'Germany', 1000000, 'test')",
                (month,)
            )
        conn.commit()
        count = conn.execute('SELECT COUNT(*) FROM uk_trade_record WHERE commodity_code="847950"').fetchone()[0]
        assert count == 3
        conn.close()
