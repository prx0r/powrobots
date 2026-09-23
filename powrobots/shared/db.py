"""Database — canonical schema for POWRobots.

Three-stage data lake: RAW → NORMALIZED → DERIVED.
All writes are append-only. Observations are immutable.
"""

import os
import sqlite3
from pathlib import Path


SCHEMA_VERSION = 1


def get_db_path() -> Path:
    return Path(os.environ.get('POWROBOTS_DB', str(Path(__file__).parent.parent.parent / 'warehouse' / 'powrobots.db')))


SCHEMA = """
-- Schema version
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Source registry
CREATE TABLE IF NOT EXISTS source_registry (
    source_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    authority TEXT,
    category TEXT,
    access_method TEXT,
    cadence TEXT,
    geographic_scope TEXT,
    historical_depth TEXT,
    requires_auth INTEGER DEFAULT 0,
    rate_limit TEXT,
    license_notes TEXT,
    tos_notes TEXT,
    expected_fields_json TEXT,
    reliability_tier TEXT DEFAULT 'C',
    collection_allowed TEXT DEFAULT 'unknown',
    enabled INTEGER DEFAULT 1
);

-- Raw blobs (content-addressed, immutable)
CREATE TABLE IF NOT EXISTS raw_blob (
    sha256 TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    content_type TEXT,
    content_length INTEGER,
    storage_path TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Acquisition receipts
CREATE TABLE IF NOT EXISTS raw_acquisition (
    acquisition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    dataset TEXT NOT NULL,
    retrieved_at TEXT NOT NULL,
    request_url TEXT,
    final_url TEXT,
    http_status INTEGER,
    etag TEXT,
    last_modified TEXT,
    content_type TEXT,
    content_length INTEGER,
    sha256 TEXT NOT NULL,
    FOREIGN KEY (sha256) REFERENCES raw_blob(sha256)
);

-- Source records (normalized from raw)
CREATE TABLE IF NOT EXISTS source_record (
    source_record_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    dataset TEXT NOT NULL,
    source_native_id TEXT,
    event_time TEXT,
    retrieved_at TEXT NOT NULL,
    normalized_json TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    raw_payload_hash TEXT NOT NULL,
    acquisition_id INTEGER,
    parser_id TEXT NOT NULL,
    parser_version TEXT NOT NULL,
    valid INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (acquisition_id) REFERENCES raw_acquisition(acquisition_id)
);

-- Source cursors
CREATE TABLE IF NOT EXISTS source_cursor (
    source_id TEXT NOT NULL,
    dataset TEXT NOT NULL,
    cursor_type TEXT,
    cursor_value TEXT,
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (source_id, dataset)
);

-- Collector run history
CREATE TABLE IF NOT EXISTS collector_run (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT,
    status TEXT DEFAULT 'running',
    raw_fetched INTEGER DEFAULT 0,
    raw_new INTEGER DEFAULT 0,
    requests_attempted INTEGER DEFAULT 0,
    requests_200 INTEGER DEFAULT 0,
    requests_403 INTEGER DEFAULT 0,
    requests_429 INTEGER DEFAULT 0,
    requests_failed INTEGER DEFAULT 0,
    source_records_new INTEGER DEFAULT 0,
    source_records_updated INTEGER DEFAULT 0,
    source_records_invalid INTEGER DEFAULT 0,
    error TEXT,
    duration_seconds REAL,
    collector_sha TEXT,
    cursor_before TEXT,
    cursor_after TEXT,
    validation_passed INTEGER DEFAULT 1,
    schema_version TEXT
);

-- Collector health
CREATE TABLE IF NOT EXISTS source_health (
    health_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    last_attempt TEXT,
    last_success TEXT,
    last_error TEXT,
    records_seen INTEGER DEFAULT 0,
    records_new INTEGER DEFAULT 0,
    records_changed INTEGER DEFAULT 0,
    records_unchanged INTEGER DEFAULT 0,
    records_invalid INTEGER DEFAULT 0,
    status TEXT DEFAULT 'unknown',
    status_reason TEXT,
    computed_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Source rights
CREATE TABLE IF NOT EXISTS source_rights (
    source_id TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'terms_review',
    licence TEXT,
    terms_url TEXT,
    notes TEXT,
    reviewed_at TEXT
);

-- === ENTITY GRAPH ===

-- Organisations (companies, institutions, integrators)
CREATE TABLE IF NOT EXISTS organisation (
    org_id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    aliases_json TEXT,
    company_number TEXT,
    sic_code TEXT,
    country_code TEXT,
    region TEXT,
    website TEXT,
    org_type TEXT,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Robot manufacturers
CREATE TABLE IF NOT EXISTS robot_manufacturer (
    manufacturer_id TEXT PRIMARY KEY,
    org_id TEXT,
    canonical_name TEXT NOT NULL,
    aliases_json TEXT,
    country_code TEXT,
    website TEXT,
    uk_distributor TEXT,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (org_id) REFERENCES organisation(org_id)
);

-- Robot families
CREATE TABLE IF NOT EXISTS robot_family (
    family_id TEXT PRIMARY KEY,
    manufacturer_id TEXT NOT NULL,
    name TEXT NOT NULL,
    robot_type TEXT,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (manufacturer_id) REFERENCES robot_manufacturer(manufacturer_id)
);

-- Robot models
CREATE TABLE IF NOT EXISTS robot_model (
    model_id TEXT PRIMARY KEY,
    manufacturer_id TEXT NOT NULL,
    family_id TEXT,
    canonical_name TEXT NOT NULL,
    aliases_json TEXT,
    robot_type TEXT,
    axes INTEGER,
    payload_kg REAL,
    reach_mm REAL,
    mass_kg REAL,
    repeatability_mm REAL,
    max_speed TEXT,
    controller TEXT,
    power_requirement TEXT,
    ingress_rating TEXT,
    mounting_options TEXT,
    launch_date TEXT,
    discontinued_date TEXT,
    status TEXT DEFAULT 'active',
    source_confidence REAL DEFAULT 1.0,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (manufacturer_id) REFERENCES robot_manufacturer(manufacturer_id),
    FOREIGN KEY (family_id) REFERENCES robot_family(family_id)
);

-- Component manufacturers
CREATE TABLE IF NOT EXISTS component_manufacturer (
    manufacturer_id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    aliases_json TEXT,
    country_code TEXT,
    website TEXT,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Components
CREATE TABLE IF NOT EXISTS component (
    component_id TEXT PRIMARY KEY,
    manufacturer_id TEXT,
    canonical_name TEXT NOT NULL,
    mpn TEXT,
    category TEXT,
    description TEXT,
    specifications_json TEXT,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (manufacturer_id) REFERENCES component_manufacturer(manufacturer_id)
);

-- Component categories (taxonomy)
CREATE TABLE IF NOT EXISTS component_category (
    category_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_category_id TEXT,
    description TEXT,
    FOREIGN KEY (parent_category_id) REFERENCES component_category(category_id)
);

-- Distributors
CREATE TABLE IF NOT EXISTS distributor (
    distributor_id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    website TEXT,
    country_code TEXT,
    has_api INTEGER DEFAULT 0,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- === BOM / RELATIONSHIPS ===

-- Product edges (generic)
CREATE TABLE IF NOT EXISTS product_relation (
    relation_id TEXT PRIMARY KEY,
    src_entity_id TEXT NOT NULL,
    dst_entity_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    confidence TEXT DEFAULT 'declared',
    evidence_json TEXT,
    source_record_id TEXT,
    valid_from TEXT,
    valid_to TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(src_entity_id, dst_entity_id, relation_type)
);

-- === MARKET DATA ===

-- Market listings (eBay, Machineseeker, etc.)
CREATE TABLE IF NOT EXISTS market_listing (
    listing_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    source_native_id TEXT NOT NULL,
    resolved_model_id TEXT,
    title TEXT,
    description TEXT,
    market TEXT,
    market_country TEXT,
    condition TEXT,
    first_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    last_seen_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (resolved_model_id) REFERENCES robot_model(model_id)
);

-- Market observations (price/stock time series)
CREATE TABLE IF NOT EXISTS market_observation (
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id TEXT,
    source_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    price REAL,
    currency TEXT DEFAULT 'GBP',
    stock TEXT,
    availability TEXT,
    condition TEXT,
    market TEXT,
    price_type TEXT,
    FOREIGN KEY (listing_id) REFERENCES market_listing(listing_id)
);

-- Component market observations
CREATE TABLE IF NOT EXISTS component_market_observation (
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_id TEXT NOT NULL,
    distributor_id TEXT,
    observed_at TEXT NOT NULL,
    currency TEXT DEFAULT 'GBP',
    unit_price_1 REAL,
    unit_price_10 REAL,
    unit_price_100 REAL,
    unit_price_1000 REAL,
    stock_qty INTEGER,
    lead_time_days INTEGER,
    lifecycle_status TEXT,
    minimum_order_qty INTEGER,
    source_record_id TEXT,
    FOREIGN KEY (component_id) REFERENCES component(component_id),
    FOREIGN KEY (distributor_id) REFERENCES distributor(distributor_id)
);

-- === UK TRADE ===

CREATE TABLE IF NOT EXISTS uk_trade_record (
    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL,
    flow TEXT NOT NULL,
    commodity_code TEXT NOT NULL,
    partner_country TEXT,
    value_gbp REAL,
    net_mass_kg REAL,
    supplementary_qty REAL,
    source_id TEXT NOT NULL,
    observed_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- === GOVERNMENT PROCUREMENT ===

CREATE TABLE IF NOT EXISTS procurement_notice (
    notice_id TEXT PRIMARY KEY,
    ocid TEXT,
    source_id TEXT NOT NULL,
    stage TEXT,
    published_at TEXT,
    buyer_name TEXT,
    buyer_org_id TEXT,
    title TEXT,
    description TEXT,
    cpv_codes TEXT,
    value_min REAL,
    value_max REAL,
    currency TEXT DEFAULT 'GBP',
    contract_start TEXT,
    contract_end TEXT,
    region TEXT,
    supplier_name TEXT,
    supplier_org_id TEXT,
    award_value REAL,
    raw_observation_id TEXT,
    observed_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (buyer_org_id) REFERENCES organisation(org_id),
    FOREIGN KEY (supplier_org_id) REFERENCES organisation(org_id)
);

-- === UKRI / GRANTS ===

CREATE TABLE IF NOT EXISTS grant_project (
    project_id TEXT PRIMARY KEY,
    programme TEXT,
    title TEXT,
    recipient_org_id TEXT,
    partners_json TEXT,
    start_date TEXT,
    end_date TEXT,
    award_gbp REAL,
    location TEXT,
    technology_tags_json TEXT,
    industry_tags_json TEXT,
    source_id TEXT NOT NULL,
    observed_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (recipient_org_id) REFERENCES organisation(org_id)
);

-- === SKILLS / LABOUR ===

CREATE TABLE IF NOT EXISTS apprenticeship_listing (
    listing_id TEXT PRIMARY KEY,
    employer TEXT,
    employer_org_id TEXT,
    training_provider TEXT,
    location TEXT,
    salary TEXT,
    qualification TEXT,
    duration TEXT,
    posting_date TEXT,
    closing_date TEXT,
    skills_json TEXT,
    robot_brands_json TEXT,
    source_id TEXT NOT NULL,
    observed_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (employer_org_id) REFERENCES organisation(org_id)
);

CREATE TABLE IF NOT EXISTS job_listing (
    listing_id TEXT PRIMARY KEY,
    employer TEXT,
    employer_org_id TEXT,
    title TEXT,
    location TEXT,
    salary_min REAL,
    salary_max REAL,
    currency TEXT DEFAULT 'GBP',
    posting_date TEXT,
    source_id TEXT NOT NULL,
    observed_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (employer_org_id) REFERENCES organisation(org_id)
);

-- === SAFETY ===

CREATE TABLE IF NOT EXISTS safety_notice (
    notice_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    product TEXT,
    brand TEXT,
    model TEXT,
    category TEXT,
    risk_level TEXT,
    failure_description TEXT,
    measure TEXT,
    recall_date TEXT,
    manufacturer_importer TEXT,
    observed_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- === DEPLOYMENT EVIDENCE ===

CREATE TABLE IF NOT EXISTS deployment_evidence (
    evidence_id TEXT PRIMARY KEY,
    observed_at TEXT NOT NULL,
    organisation_id TEXT,
    facility_id TEXT,
    robot_manufacturer_id TEXT,
    robot_model_id TEXT,
    robot_count INTEGER,
    application TEXT,
    evidence_type TEXT,
    confidence REAL DEFAULT 1.0,
    source_id TEXT,
    source_record_id TEXT,
    FOREIGN KEY (organisation_id) REFERENCES organisation(org_id),
    FOREIGN KEY (robot_manufacturer_id) REFERENCES robot_manufacturer(manufacturer_id),
    FOREIGN KEY (robot_model_id) REFERENCES robot_model(model_id)
);

-- === COMPANIES HOUSE ===

CREATE TABLE IF NOT EXISTS company_filing (
    filing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_number TEXT NOT NULL,
    filing_type TEXT,
    filing_date TEXT,
    description TEXT,
    source_id TEXT NOT NULL,
    observed_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- === CHANGE EVENTS ===

CREATE TABLE IF NOT EXISTS change_event (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    field TEXT NOT NULL,
    old_value TEXT,
    new_value TEXT,
    first_observed_at TEXT,
    detected_at TEXT NOT NULL DEFAULT (datetime('now')),
    source_id TEXT
);

-- === ROS / ROBOT DESCRIPTIONS ===

CREATE TABLE IF NOT EXISTS robot_description (
    description_id TEXT PRIMARY KEY,
    model_id TEXT,
    format TEXT,
    source_repo TEXT,
    commit_sha TEXT,
    licence TEXT,
    links_json TEXT,
    joints_json TEXT,
    transmissions_json TEXT,
    hardware_interfaces_json TEXT,
    observed_at TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (model_id) REFERENCES robot_model(model_id)
);

-- === INDEXES ===

CREATE INDEX IF NOT EXISTS idx_source_record_source ON source_record(source_id);
CREATE INDEX IF NOT EXISTS idx_source_record_native ON source_record(source_native_id);
CREATE INDEX IF NOT EXISTS idx_raw_acq_source ON raw_acquisition(source_id);
CREATE INDEX IF NOT EXISTS idx_market_listing_model ON market_listing(resolved_model_id);
CREATE INDEX IF NOT EXISTS idx_market_obs_listing ON market_observation(listing_id);
CREATE INDEX IF NOT EXISTS idx_market_obs_time ON market_observation(observed_at);
CREATE INDEX IF NOT EXISTS idx_comp_obs_component ON component_market_observation(component_id);
CREATE INDEX IF NOT EXISTS idx_comp_obs_distributor ON component_market_observation(distributor_id);
CREATE INDEX IF NOT EXISTS idx_uk_trade_commodity ON uk_trade_record(commodity_code);
CREATE INDEX IF NOT EXISTS idx_uk_trade_month ON uk_trade_record(month);
CREATE INDEX IF NOT EXISTS idx_procurement_buyer ON procurement_notice(buyer_org_id);
CREATE INDEX IF NOT EXISTS idx_procurement_published ON procurement_notice(published_at);
CREATE INDEX IF NOT EXISTS idx_grant_recipient ON grant_project(recipient_org_id);
CREATE INDEX IF NOT EXISTS idx_deployment_manufacturer ON deployment_evidence(robot_manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_deployment_model ON deployment_evidence(robot_model_id);
CREATE INDEX IF NOT EXISTS idx_relation_src ON product_relation(src_entity_id);
CREATE INDEX IF NOT EXISTS idx_relation_dst ON product_relation(dst_entity_id);
CREATE INDEX IF NOT EXISTS idx_robot_model_manufacturer ON robot_model(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_component_manufacturer ON component(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_company_filing_number ON company_filing(company_number);
CREATE INDEX IF NOT EXISTS idx_change_event_entity ON change_event(entity_id);
"""


def _enable_foreign_keys(conn):
    conn.execute("PRAGMA foreign_keys=ON")


def get_db():
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    _enable_foreign_keys(conn)
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def init_db():
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    _enable_foreign_keys(conn)
    conn.executescript(SCHEMA)
    conn.commit()
    print(f'Database initialized: {db_path}')
    return conn


def status():
    conn = get_db()
    tables = [t[0] for t in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name != 'schema_version' ORDER BY name"
    ).fetchall()]
    print('=== DATABASE STATUS ===')
    for t in tables:
        try:
            c = conn.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]
            print(f'  {t:40s} {c:>10,}')
        except:
            print(f'  {t:40s} {"ERROR":>10}')
    conn.close()


# ─── Seed Data ──────────────────────────────────────────────

# All 15 powrobots sources with their access method and rights status.
# Sources that need API keys are marked 'approved' (key required, review passed).
# Open sources are marked 'open'.
SOURCES_SEED = [
    # P0 — Open / No Auth
    {
        'source_id': 'hmrc_traders',
        'name': 'HMRC Trader Search',
        'authority': 'HMRC',
        'category': 'uk_trade',
        'access_method': 'web_scrape',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'B',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'HMRC UK Trade Info — trader search for HS 847950',
    },
    {
        'source_id': 'hmrc_trade',
        'name': 'HMRC Trade Statistics',
        'authority': 'HMRC',
        'category': 'uk_trade',
        'access_method': 'web_scrape',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'B',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'HMRC UK Trade Info — trade statistics index page',
    },
    {
        'source_id': 'ukri_gtr',
        'name': 'UKRI Gateway to Research',
        'authority': 'UKRI',
        'category': 'grants',
        'access_method': 'api',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'A',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'Public API — robotics/automation research projects',
    },
    {
        'source_id': 'rbtx',
        'name': 'RBTX Robot Marketplace',
        'authority': 'RBTX/igus',
        'category': 'marketplace',
        'access_method': 'web_scrape',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'B',
        'rights_status': 'open',
        'licence': 'TOS_review',
        'notes': 'Low-cost robot marketplace — UK + China pricing',
    },
    {
        'source_id': 'opss_safety',
        'name': 'OPSS Safety Alerts',
        'authority': 'OPSS',
        'category': 'safety',
        'access_method': 'web_scrape',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'A',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'GOV.UK product safety alerts — machinery category',
    },
    {
        'source_id': 'bara_directory',
        'name': 'BARA/Automate UK Directory',
        'authority': 'BARA',
        'category': 'integrators',
        'access_method': 'web_scrape',
        'cadence': 'weekly',
        'requires_auth': 0,
        'reliability_tier': 'B',
        'rights_status': 'open',
        'licence': 'TOS_review',
        'notes': 'British Automation & Robot Association member directory',
    },
    {
        'source_id': 'bgs_minerals',
        'name': 'BGS World Mineral Statistics',
        'authority': 'BGS',
        'category': 'minerals',
        'access_method': 'web_scrape',
        'cadence': 'weekly',
        'requires_auth': 0,
        'reliability_tier': 'A',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'UK critical minerals supply data',
    },
    {
        'source_id': 'contracts_finder',
        'name': 'Contracts Finder',
        'authority': 'Contracts Finder',
        'category': 'procurement',
        'access_method': 'api',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'A',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'UK public procurement — robotics/automation contracts',
    },
    {
        'source_id': 'ons_ppi',
        'name': 'ONS Producer Price Index',
        'authority': 'ONS',
        'category': 'prices',
        'access_method': 'web_scrape',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'A',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'UK inflation/price indices — electronics category',
    },
    {
        'source_id': 'find_apprenticeship',
        'name': 'Find an Apprenticeship',
        'authority': 'Education and Skills Funding Agency',
        'category': 'labour',
        'access_method': 'web_scrape',
        'cadence': 'daily',
        'requires_auth': 0,
        'reliability_tier': 'B',
        'rights_status': 'open',
        'licence': 'OGL',
        'notes': 'UK robotics/automation apprenticeship listings',
    },
    # P0 — Needs API Key (free)
    {
        'source_id': 'companies_house',
        'name': 'Companies House',
        'authority': 'Companies House',
        'category': 'corporate',
        'access_method': 'api',
        'cadence': 'daily',
        'requires_auth': 1,
        'reliability_tier': 'A',
        'rights_status': 'approved',
        'licence': 'OGL',
        'notes': 'UK company filings — key env: COMPANIES_HOUSE_API_KEY',
    },
    {
        'source_id': 'mouser',
        'name': 'Mouser Electronics',
        'authority': 'Mouser',
        'category': 'components',
        'access_method': 'api',
        'cadence': 'daily',
        'requires_auth': 1,
        'reliability_tier': 'A',
        'rights_status': 'approved',
        'licence': 'TOS_review',
        'notes': 'Electronic component pricing/stock — key env: MOUSER_API_KEY',
    },
    {
        'source_id': 'farnell',
        'name': 'Farnell/element14',
        'authority': 'Farnell',
        'category': 'components',
        'access_method': 'api',
        'cadence': 'daily',
        'requires_auth': 1,
        'reliability_tier': 'A',
        'rights_status': 'approved',
        'licence': 'TOS_review',
        'notes': 'UK electronic component catalogue — key env: FARNELL_API_KEY',
    },
    {
        'source_id': 'lcsc',
        'name': 'LCSC Electronics',
        'authority': 'LCSC',
        'category': 'components',
        'access_method': 'api',
        'cadence': 'daily',
        'requires_auth': 1,
        'reliability_tier': 'A',
        'rights_status': 'approved',
        'licence': 'TOS_review',
        'notes': 'Chinese electronic component pricing — key env: LCSC_API_KEY',
    },
    {
        'source_id': 'ebay_uk',
        'name': 'eBay UK',
        'authority': 'eBay',
        'category': 'aftermarket',
        'access_method': 'api',
        'cadence': 'daily',
        'requires_auth': 1,
        'reliability_tier': 'B',
        'rights_status': 'approved',
        'licence': 'TOS_review',
        'notes': 'UK secondhand robotics equipment — key env: EBAY_APP_ID',
    },
]


def seed_rights(conn=None):
    """Seed source_rights table for all 15 collectors.

    Returns (inserted, skipped) counts.
    """
    close = False
    if conn is None:
        conn = get_db()
        close = True
    inserted = 0
    skipped = 0
    for src in SOURCES_SEED:
        exists = conn.execute(
            "SELECT 1 FROM source_rights WHERE source_id = ?", (src['source_id'],)
        ).fetchone()
        if exists:
            skipped += 1
            continue
        conn.execute(
            "INSERT INTO source_rights (source_id, status, licence, notes, reviewed_at) "
            "VALUES (?, ?, ?, ?, datetime('now'))",
            (src['source_id'], src['rights_status'], src['licence'], src['notes']),
        )
        inserted += 1
    conn.commit()
    if close:
        conn.close()
    return inserted, skipped


def seed_registry(conn=None):
    """Seed source_registry table for all 15 collectors.

    Returns (inserted, skipped) counts.
    """
    close = False
    if conn is None:
        conn = get_db()
        close = True
    inserted = 0
    skipped = 0
    for src in SOURCES_SEED:
        exists = conn.execute(
            "SELECT 1 FROM source_registry WHERE source_id = ?", (src['source_id'],)
        ).fetchone()
        if exists:
            skipped += 1
            continue
        conn.execute(
            "INSERT INTO source_registry "
            "(source_id, name, authority, category, access_method, cadence, "
            " requires_auth, reliability_tier, collection_allowed, enabled) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (src['source_id'], src['name'], src['authority'], src['category'],
             src['access_method'], src['cadence'], src['requires_auth'],
             src['reliability_tier'],
             'open' if src['rights_status'] == 'open' else 'needs_key',
             1),
        )
        inserted += 1
    conn.commit()
    if close:
        conn.close()
    return inserted, skipped


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        status()
    else:
        init_db()
