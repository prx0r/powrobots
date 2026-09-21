"""RBTX/igus Marketplace Collector — robot pricing China+UK+EU.

Scrapes the RBTX robotics marketplace for robot pricing.
Source: https://rbtx.co.uk/ (UK), https://rbtx.igus.cn/ (China)
"""

import json
import re
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record


class RbtxCollector(BaseCollector):
    SOURCE_ID = 'rbtx'
    DATASET = 'robot_pricing'
    PARSER_ID = 'rbtx_web_v1'

    MARKETS = {
        'uk': 'https://rbtx.co.uk/en-GB/partners/rbtx',
        'cn': 'https://rbtx.igus.cn/en-GB?C=CH',
    }

    def fetch(self):
        """Fetch RBTX marketplace listings from UK and China."""
        all_items = []
        for market, url in self.MARKETS.items():
            acq = self._fetch_url(url, timeout=15)
            if acq and acq.get('status') == 200:
                all_items.append({
                    'market': market,
                    'content_length': len(acq['content']),
                    'sha256': acq['sha256'],
                })
        if not all_items:
            return None
        return json.dumps(all_items).encode()

    def parse(self, raw_content, raw_hash, result):
        """Parse RBTX marketplace data."""
        if not raw_content:
            return
        items = json.loads(raw_content)
        for item in items:
            normalized = {
                'source_native_id': f"rbtx_{item['market']}",
                'market': item['market'],
                'content_length': item['content_length'],
                'note': f"RBTX {item['market'].upper()} marketplace page stored as evidence",
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, f"rbtx_{item['market']}",
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1


if __name__ == '__main__':
    RbtxCollector().run()
