"""BGS Minerals Collector — British Geological Survey data.

Uses the BGS World Mineral Statistics API.
Source: https://www.bgs.ac.uk/mineralsuk/
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record

# Materials relevant to robotics
MATERIALS = [
    'copper', 'aluminium', 'steel', 'neodymium', 'praseodymium',
    'dysprosium', 'cobalt', 'lithium', 'nickel', 'silicon',
]


class BgsMineralsCollector(BaseCollector):
    SOURCE_ID = 'bgs_minerals'
    DATASET = 'mineral_production'
    PARSER_ID = 'bgs_api_v1'

    def fetch(self):
        """Fetch BGS mineral production data."""
        all_data = []
        for material in MATERIALS[:3]:  # Limit for initial run
            url = f'https://www.bgs.ac.uk/mineralsuk/api/minerals/{material}'
            acq = self._fetch_url(url, timeout=15)
            if acq and acq.get('status') == 200:
                all_data.append({
                    'material': material,
                    'content_length': len(acq['content']),
                    'sha256': acq['sha256'],
                })
        if not all_data:
            return None
        return json.dumps(all_data).encode()

    def parse(self, raw_content, raw_hash, result):
        """Parse BGS mineral data."""
        if not raw_content:
            return
        data = json.loads(raw_content)
        for item in data:
            normalized = {
                'source_native_id': f"bgs_{item['material']}",
                'material': item['material'],
                'content_length': item['content_length'],
                'note': f"BGS mineral production data for {item['material']}",
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, f"bgs_{item['material']}",
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1


if __name__ == '__main__':
    BgsMineralsCollector().run()
