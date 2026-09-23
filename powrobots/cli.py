"""CLI — powrobots command interface."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# All 15 collectors — source_id → class path
COLLECTORS = {
    'companies_house': 'powrobots.collectors.companies_house:CompaniesHouseCollector',
    'ukri_gtr': 'powrobots.collectors.ukri_gtr:UkriGtrCollector',
    'mouser': 'powrobots.collectors.mouser:MouserCollector',
    'farnell': 'powrobots.collectors.farnell:FarnellCollector',
    'lcsc': 'powrobots.collectors.lcsc:LcscCollector',
    'ebay_uk': 'powrobots.collectors.ebay_uk:EbayUkCollector',
    'hmrc_trade': 'powrobots.collectors.hmrc_trade:HmrcTradeCollector',
    'hmrc_traders': 'powrobots.collectors.hmrc_traders:HmrcTraderCollector',
    'rbtx': 'powrobots.collectors.rbtx:RbtxCollector',
    'contracts_finder': 'powrobots.collectors.contracts_finder:ContractsFinderCollector',
    'opss_safety': 'powrobots.collectors.opss_safety:OpsSafetyCollector',
    'bara_directory': 'powrobots.collectors.bara_directory:BaraDirectoryCollector',
    'find_apprenticeship': 'powrobots.collectors.apprenticeships:ApprenticeshipCollector',
    'ons_ppi': 'powrobots.collectors.ons_ppi:OnsPpiCollector',
    'bgs_minerals': 'powrobots.collectors.bgs_minerals:BgsMineralsCollector',
}


def cmd_status(args):
    from powrobots.shared.db import status
    status()


def cmd_sources(args):
    from powrobots.shared.db import get_db
    conn = get_db()
    rows = conn.execute(
        "SELECT source_id, name, category, reliability_tier, enabled "
        "FROM source_registry ORDER BY source_id"
    ).fetchall()
    if not rows:
        print('  No sources registered. Run: powrobots seed')
        conn.close()
        return
    print(f'  {"Source ID":30s} {"Name":30s} {"Category":20s} {"Tier":5s} {"On":4s}')
    print(f'  {"-"*30} {"-"*30} {"-"*20} {"-"*5} {"-"*4}')
    for r in rows:
        print(f'  {r[0]:30s} {(r[1] or ""):30s} {(r[2] or ""):20s} {(r[3] or ""):5s} {"Y" if r[4] else "N":4s}')
    print(f'\n  {len(rows)} sources registered')
    conn.close()


def cmd_collect(args):
    source_id = args.source
    if source_id == 'all':
        sources = list(COLLECTORS.keys())
    elif source_id in COLLECTORS:
        sources = [source_id]
    else:
        print(f'Unknown source: {source_id}')
        print(f'Available: {", ".join(sorted(COLLECTORS.keys()))}')
        return

    for sid in sources:
        class_path = COLLECTORS[sid]
        module_path, class_name = class_path.rsplit(':', 1)
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        collector = cls()
        result = collector.run()
        print(f'  Result: new={result.records_new} unchanged={result.records_unchanged} errors={result.errors}\n')


def cmd_seed(args):
    from powrobots.shared.db import get_db, seed_rights, seed_registry
    conn = get_db()
    r_ins, r_skip = seed_rights(conn)
    s_ins, s_skip = seed_registry(conn)
    conn.close()
    print(f'  source_rights:  +{r_ins} inserted, {r_skip} skipped')
    print(f'  source_registry: +{s_ins} inserted, {s_skip} skipped')
    print(f'  Total: {r_ins + s_ins} new rows')


def cmd_validate(args):
    from powrobots.shared.db import get_db
    conn = get_db()
    checks = []

    tables = [r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]
    checks.append(('Tables exist', len(tables) >= 25, f'{len(tables)} tables'))

    mfg_count = conn.execute('SELECT COUNT(*) FROM robot_manufacturer').fetchone()[0]
    checks.append(('Manufacturers seeded', mfg_count > 0, f'{mfg_count} manufacturers'))

    model_count = conn.execute('SELECT COUNT(*) FROM robot_model').fetchone()[0]
    checks.append(('Models exist', model_count >= 0, f'{model_count} models'))

    rights_count = conn.execute('SELECT COUNT(*) FROM source_rights').fetchone()[0]
    checks.append(('Source rights configured', rights_count > 0, f'{rights_count} sources'))

    registry_count = conn.execute('SELECT COUNT(*) FROM source_registry').fetchone()[0]
    checks.append(('Source registry populated', registry_count > 0, f'{registry_count} sources'))

    run_count = conn.execute('SELECT COUNT(*) FROM collector_run').fetchone()[0]
    checks.append(('Collectors have run', run_count > 0, f'{run_count} runs recorded'))

    conn.close()

    print('=== VALIDATION ===')
    all_pass = True
    for name, passed, detail in checks:
        status = 'PASS' if passed else 'FAIL'
        if not passed:
            all_pass = False
        print(f'  [{status}] {name}: {detail}')
    print(f'\nOverall: {"PASS" if all_pass else "FAIL"}')


def cmd_health(args):
    """Show what powops will see — last collector run per source."""
    from powrobots.shared.db import get_db
    conn = get_db()
    rows = conn.execute("""
        SELECT source_id, started_at, finished_at, status,
               source_records_new, error, duration_seconds
        FROM collector_run
        WHERE (source_id, run_id) IN (
            SELECT source_id, MAX(run_id) FROM collector_run GROUP BY source_id
        )
        ORDER BY source_id
    """).fetchall()
    if not rows:
        print('  No collector runs recorded. Run: powrobots collect all')
        conn.close()
        return
    print(f'  {"SOURCE":24s} {"STATUS":10s} {"LAST RUN":20s} {"NEW":6s} {"DUR":8s}')
    print(f'  {"-"*24} {"-"*10} {"-"*20} {"-"*6} {"-"*8}')
    for r in rows:
        sid, started, finished, status, new, err, dur = r
        started_short = (started or '')[:19]
        dur_str = f'{dur:.1f}s' if dur else '—'
        new_str = str(new) if new else '0'
        print(f'  {sid:24s} {status:10s} {started_short:20s} {new_str:6s} {dur_str:8s}')
    print()
    conn.close()


def cmd_models(args):
    from powrobots.shared.db import get_db
    conn = get_db()
    rows = conn.execute(
        'SELECT model_id, canonical_name, manufacturer_id, robot_type, axes, payload_kg, reach_mm '
        'FROM robot_model ORDER BY manufacturer_id, canonical_name'
    ).fetchall()
    if not rows:
        print('  No models found. Run: powrobots seed')
        conn.close()
        return
    print(f'  {"MODEL ID":30s} {"NAME":30s} {"MANUFACTURER":16s} {"TYPE":12s} {"AXES":5s} {"PAYLOAD":8s} {"REACH":8s}')
    print(f'  {"-"*30} {"-"*30} {"-"*16} {"-"*12} {"-"*5} {"-"*8} {"-"*8}')
    for r in rows:
        mid = (r[0] or '')[:28]
        name = (r[1] or '')[:28]
        mfg = (r[2] or '')[:14]
        rtype = (r[3] or '')[:10]
        axes = str(r[4] or '')[:3]
        payload = f'{r[5]:.1f}kg' if r[5] else '—'
        reach = f'{r[6]:.0f}mm' if r[6] else '—'
        print(f'  {mid:30s} {name:30s} {mfg:16s} {rtype:12s} {axes:5s} {payload:8s} {reach:8s}')
    print(f'\n  {len(rows)} models')
    conn.close()


def cmd_components(args):
    from powrobots.shared.db import get_db
    conn = get_db()
    rows = conn.execute(
        'SELECT component_id, canonical_name, mpn, category, manufacturer_id '
        'FROM component ORDER BY category, canonical_name'
    ).fetchall()
    if not rows:
        print('  No components found. Run: powrobots seed')
        conn.close()
        return
    print(f'  {"COMPONENT ID":24s} {"NAME":28s} {"MPN":20s} {"CATEGORY":16s} {"MANUFACTURER":16s}')
    print(f'  {"-"*24} {"-"*28} {"-"*20} {"-"*16} {"-"*16}')
    for r in rows:
        cid = (r[0] or '')[:22]
        name = (r[1] or '')[:26]
        mpn = (r[2] or '')[:18]
        cat = (r[3] or '')[:14]
        mfg = (r[4] or '')[:14]
        print(f'  {cid:24s} {name:28s} {mpn:20s} {cat:16s} {mfg:16s}')
    print(f'\n  {len(rows)} components')
    conn.close()


def cmd_organisations(args):
    from powrobots.shared.db import get_db
    conn = get_db()
    rows = conn.execute(
        'SELECT org_id, canonical_name, country_code, org_type '
        'FROM organisation ORDER BY org_type, canonical_name LIMIT 50'
    ).fetchall()
    count = conn.execute('SELECT COUNT(*) FROM organisation').fetchone()[0]
    if not rows:
        print('  No organisations found.')
        conn.close()
        return
    print(f'  {"ORG ID":30s} {"NAME":36s} {"COUNTRY":8s} {"TYPE":16s}')
    print(f'  {"-"*30} {"-"*36} {"-"*8} {"-"*16}')
    for r in rows:
        oid = (r[0] or '')[:28]
        name = (r[1] or '')[:34]
        cc = (r[2] or '')[:6]
        otype = (r[3] or '')[:14]
        print(f'  {oid:30s} {name:36s} {cc:8s} {otype:16s}')
    if count > 50:
        print(f'\n  Showing 50 of {count} organisations')
    else:
        print(f'\n  {count} organisations')
    conn.close()


def cmd_robots(args):
    from powrobots.shared.db import get_db
    conn = get_db()
    mfg_count = conn.execute('SELECT COUNT(*) FROM robot_manufacturer').fetchone()[0]
    model_count = conn.execute('SELECT COUNT(*) FROM robot_model').fetchone()[0]
    rel_count = conn.execute('SELECT COUNT(*) FROM product_relation').fetchone()[0]
    comp_count = conn.execute('SELECT COUNT(*) FROM component').fetchone()[0]
    org_count = conn.execute('SELECT COUNT(*) FROM organisation').fetchone()[0]
    print(f'  === Entity Graph Summary ===')
    print(f'  Organisations:    {org_count:>6}')
    print(f'  Manufacturers:    {mfg_count:>6}')
    print(f'  Robot models:     {model_count:>6}')
    print(f'  Components:       {comp_count:>6}')
    print(f'  Relations:        {rel_count:>6}')
    print()
    # Show top manufacturers by model count
    rows = conn.execute('''
        SELECT m.canonical_name, COUNT(rm.model_id) as models
        FROM robot_manufacturer m
        LEFT JOIN robot_model rm ON rm.manufacturer_id = m.manufacturer_id
        GROUP BY m.manufacturer_id
        ORDER BY models DESC LIMIT 10
    ''').fetchall()
    print(f'  Top manufacturers by model count:')
    for name, count in rows:
        print(f'    {name:30s} {count:>3} models')
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='POWRobots CLI')
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('status', help='Show database row counts')
    sub.add_parser('sources', help='List registered sources')
    sub.add_parser('seed', help='Seed source_rights + source_registry')
    sub.add_parser('validate', help='Run validation checks')
    sub.add_parser('health', help='Show last collector run per source')
    sub.add_parser('robots', help='Entity graph summary')
    sub.add_parser('models', help='List robot models')
    sub.add_parser('components', help='List components')
    sub.add_parser('organisations', help='List organisations (first 50)')

    collect_p = sub.add_parser('collect', help='Run a collector')
    collect_p.add_argument('source', help='Source ID or "all"')

    args = parser.parse_args()
    if args.command == 'status':
        cmd_status(args)
    elif args.command == 'sources':
        cmd_sources(args)
    elif args.command == 'seed':
        cmd_seed(args)
    elif args.command == 'collect':
        cmd_collect(args)
    elif args.command == 'validate':
        cmd_validate(args)
    elif args.command == 'health':
        cmd_health(args)
    elif args.command == 'robots':
        cmd_robots(args)
    elif args.command == 'models':
        cmd_models(args)
    elif args.command == 'components':
        cmd_components(args)
    elif args.command == 'organisations':
        cmd_organisations(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
