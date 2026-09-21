"""Seed loader — populate entity graph from YAML seeds and cloned repos."""

import os
import sys
import yaml
import json
import hashlib
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from powrobots.shared.persist import (
    upsert_organisation, upsert_robot_manufacturer, upsert_robot_model,
    upsert_component, insert_relation, insert_source_record, get_db
)
from powrobots.shared.db import _enable_foreign_keys


def load_manufacturers(seed_path):
    """Load robot manufacturers from YAML seed."""
    with open(seed_path) as f:
        data = yaml.safe_load(f)
    count = 0
    for m in data:
        upsert_robot_manufacturer(
            m['id'], m['name'],
            country_code=m.get('country', ''),
            website=m.get('website', ''),
            aliases=[m['name']] if m['name'] != m['id'] else []
        )
        count += 1
    print(f'  Loaded {count} manufacturers')
    return count


def load_manufacturers_to_organisations(seed_path):
    """Also create organisation entries for manufacturers."""
    with open(seed_path) as f:
        data = yaml.safe_load(f)
    count = 0
    for m in data:
        upsert_organisation(
            m['id'], m['name'],
            country_code=m.get('country', ''),
            website=m.get('website', ''),
            org_type='robot_manufacturer'
        )
        count += 1
    print(f'  Loaded {count} organisations')
    return count


def load_component_categories(seed_path):
    """Load component categories from YAML seed."""
    with open(seed_path) as f:
        data = yaml.safe_load(f)
    conn = get_db()
    count = 0
    for c in data:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO component_category (category_id, name, parent_category_id) "
                "VALUES (?, ?, ?)",
                (c['id'], c['name'], c.get('parent'))
            )
            count += 1
        except Exception:
            pass
    conn.commit()
    conn.close()
    print(f'  Loaded {count} component categories')
    return count


def load_component_basket(seed_path):
    """Load component basket from YAML seed."""
    with open(seed_path) as f:
        data = yaml.safe_load(f)
    conn = get_db()
    # Ensure component manufacturers exist
    mfr_ids = set()
    for category, items in data.items():
        if not isinstance(items, list):
            continue
        for item in items:
            mfr = item.get('manufacturer', '')
            if mfr and mfr not in mfr_ids:
                mfr_ids.add(mfr)
                try:
                    conn.execute(
                        "INSERT OR IGNORE INTO component_manufacturer (manufacturer_id, canonical_name) "
                        "VALUES (?, ?)", (mfr, mfr)
                    )
                except Exception:
                    pass
    conn.commit()
    count = 0
    for category, items in data.items():
        if not isinstance(items, list):
            continue
        for item in items:
            comp_id = hashlib.sha256(
                f"{item.get('name', '')}:{item.get('manufacturer', '')}".encode()
            ).hexdigest()[:16]
            try:
                conn.execute(
                    "INSERT OR IGNORE INTO component (component_id, manufacturer_id, canonical_name, category) "
                    "VALUES (?, ?, ?, ?)",
                    (comp_id, item.get('manufacturer', ''), item.get('name', ''),
                     item.get('category', category))
                )
                count += 1
            except Exception:
                pass
    conn.commit()
    conn.close()
    print(f'  Loaded {count} components from basket')
    return count


def load_chinese_stocks(seed_path):
    """Load Chinese robotics stocks from YAML seed."""
    with open(seed_path) as f:
        data = yaml.safe_load(f)
    conn = get_db()
    count = 0
    for stock in data:
        # Store as organisation with stock metadata
        upsert_organisation(
            stock['id'], stock['name'],
            country_code=stock.get('country', 'CN'),
            website='',
            org_type='listed_company'
        )
        # Store the stock info in a source record for later use
        insert_source_record(
            'powrobots_seeds', 'chinese_stocks', stock['id'],
            {
                'source_native_id': stock['id'],
                'name': stock['name'],
                'tickers': stock.get('tickers', []),
                'pow_node': stock.get('pow_node', ''),
                'notes': stock.get('notes', ''),
            },
            'seed', 'seed_loader_v1'
        )
        count += 1
    print(f'  Loaded {count} Chinese stocks')
    return count


def load_ros_repos(seed_path):
    """Load ROS repository metadata from YAML seed."""
    with open(seed_path) as f:
        data = yaml.safe_load(f)
    count = 0
    for repo in data:
        # Create robot models from ROS repo entries
        manufacturer = repo.get('manufacturer', '')
        for model_name in repo.get('models', []):
            model_id = f"{manufacturer}-{model_name}".lower().replace(' ', '-')
            upsert_robot_model(
                model_id, manufacturer, model_name,
                robot_type='industrial_arm'
            )
            # Store description reference
            insert_relation(
                model_id, f"ros:{repo['id']}", 'HAS_DESCRIPTION',
                confidence='declared',
                evidence_json=json.dumps({
                    'repo': repo.get('url', ''),
                    'format': repo.get('format', ''),
                    'licence': repo.get('licence', '')
                })
            )
            count += 1
    print(f'  Loaded {count} robot models from ROS repos')
    return count


def scan_mujoco_menagerie(menagerie_path):
    """Scan MuJoCo Menagerie cloned repo for robot models."""
    count = 0
    if not os.path.exists(menagerie_path):
        print(f'  MuJoCo Menagerie not found at {menagerie_path}')
        return 0
    # Ensure 'unknown' manufacturer exists
    upsert_robot_manufacturer('unknown', 'Unknown')
    for model_dir in sorted(Path(menagerie_path).iterdir()):
        if not model_dir.is_dir():
            continue
        xml_files = list(model_dir.glob('*.xml'))
        if not xml_files:
            continue
        # Extract model info from directory name
        model_name = model_dir.name
        # Try to find manufacturer info from README
        readme = model_dir / 'README.md'
        manufacturer = ''
        if readme.exists():
            text = readme.read_text(errors='replace')[:500]
            for mfg in ['FANUC', 'KUKA', 'ABB', 'Universal Robots', 'UR', 'Franka',
                         'Yaskawa', 'Staubli', 'Kinova', 'Robotiq', 'ANYbotics',
                         'Boston Dynamics', 'Unitree', 'DOBOT', 'igus']:
                if mfg.lower() in text.lower():
                    manufacturer = mfg
                    break

        model_id = f"mj_{model_name}".replace(' ', '-').replace('.', '')
        mfr_id = manufacturer.lower().replace(' ', '_') if manufacturer else 'unknown'
        # Ensure manufacturer exists
        upsert_robot_manufacturer(mfr_id, manufacturer or 'Unknown')
        upsert_robot_model(model_id, mfr_id, model_name, robot_type='robot')
        count += 1
    print(f'  Scanned {count} MuJoCo Menagerie models')
    return count


def scan_fanuc_description(fanuc_path):
    """Scan FANUC description repo for robot models."""
    count = 0
    if not os.path.exists(fanuc_path):
        print(f'  FANUC description not found at {fanuc_path}')
        return 0
    upsert_robot_manufacturer('fanuc', 'FANUC')
    for model_dir in sorted(Path(fanuc_path).iterdir()):
        if not model_dir.is_dir():
            continue
        urdf_files = list(model_dir.glob('**/*.urdf'))
        xacro_files = list(model_dir.glob('**/*.xacro'))
        if not urdf_files and not xacro_files:
            continue
        model_name = model_dir.name
        model_id = f"fanuc_{model_name}".replace(' ', '_')
        upsert_robot_model(model_id, 'fanuc', model_name, robot_type='industrial_arm')
        count += 1
    print(f'  Scanned {count} FANUC models')
    return count


def scan_kuka_descriptions(kuka_path):
    """Scan KUKA descriptions repo."""
    count = 0
    if not os.path.exists(kuka_path):
        print(f'  KUKA descriptions not found at {kuka_path}')
        return 0
    upsert_robot_manufacturer('kuka', 'KUKA')
    for model_dir in sorted(Path(kuka_path).iterdir()):
        if not model_dir.is_dir():
            continue
        urdf_files = list(model_dir.glob('**/*.urdf'))
        xacro_files = list(model_dir.glob('**/*.xacro'))
        if not urdf_files and not xacro_files:
            continue
        model_name = model_dir.name
        model_id = f"kuka_{model_name}".replace(' ', '_')
        upsert_robot_model(model_id, 'kuka', model_name, robot_type='industrial_arm')
        count += 1
    print(f'  Scanned {count} KUKA models')
    return count


def main():
    base = Path(__file__).parent.parent
    seeds = base / 'powrobots' / 'seeds'
    vendor = base / 'vendor_repos'

    print('=== SEED LOADER ===\n')

    print('[1] Organisations from manufacturers...')
    load_manufacturers_to_organisations(seeds / 'manufacturers.yml')

    print('[2] Robot manufacturers...')
    load_manufacturers(seeds / 'manufacturers.yml')

    print('[3] Component categories...')
    load_component_categories(seeds / 'component_categories.yml')

    print('[4] Component basket...')
    load_component_basket(seeds / 'component_basket.yml')

    print('[5] Chinese stocks...')
    load_chinese_stocks(seeds / 'chinese_stocks.yml')

    print('[6] ROS repository models...')
    load_ros_repos(seeds / 'ros_repositories.yml')

    print('[7] MuJoCo Menagerie...')
    scan_mujoco_menagerie(vendor / 'mujoco_menagerie')

    print('[8] FANUC description...')
    scan_fanuc_description(vendor / 'fanuc_description')

    print('[9] KUKA descriptions...')
    scan_kuka_descriptions(vendor / 'kuka_robot_descriptions')

    # DB status
    print('\n=== DATABASE STATUS ===')
    conn = get_db()
    for table in ['organisation', 'robot_manufacturer', 'robot_model',
                   'component', 'component_category', 'product_relation', 'source_record']:
        try:
            count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
            print(f'  {table:35s} {count:>8,}')
        except:
            print(f'  {table:35s} {"ERROR":>8}')
    conn.close()


if __name__ == '__main__':
    main()
