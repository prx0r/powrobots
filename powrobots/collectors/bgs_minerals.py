"""BGS Minerals Collector — British Geological Survey data.

Scrapes the BGS Minerals UK statistics page.
Source: https://www.bgs.ac.uk/mineralsuk/statistics/
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record


class BgsMineralsCollector(BaseCollector):
    SOURCE_ID = 'bgs_minerals'
    DATASET = 'mineral_production'
    PARSER_ID = 'bgs_web_v1'

    def fetch(self):
        """Fetch BGS minerals statistics page."""
        acq = self._fetch_url('https://www.bgs.ac.uk/mineralsuk/statistics/', timeout=30)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        normalized = {
            'source_native_id': 'bgs_minerals_statistics',
            'content_type': 'html',
            'content_length': len(raw_content),
            'note': 'BGS World Mineral Statistics page stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'minerals_statistics',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    BgsMineralsCollector().run()
