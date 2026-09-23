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


def main():
    parser = argparse.ArgumentParser(description='POWRobots CLI')
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('status', help='Show database row counts')
    sub.add_parser('sources', help='List registered sources')
    sub.add_parser('seed', help='Seed source_rights + source_registry')
    sub.add_parser('validate', help='Run validation checks')
    sub.add_parser('health', help='Show last collector run per source')

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
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
