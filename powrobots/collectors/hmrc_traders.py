"""HMRC UK Trade Info Trader Collector — open, no auth.

Searches for specific traders by commodity code.
Source: https://www.uktradeinfo.com/search/traders/
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation


class HmrcTraderCollector(BaseCollector):
    SOURCE_ID = 'hmrc_traders'
    DATASET = 'trader_data'
    PARSER_ID = 'hmrc_tradeinfo_v1'

    def fetch(self):
        """Fetch HMRC trader search page for robotics commodity codes."""
        acq = self._fetch_url(
            'https://www.uktradeinfo.com/search/traders/?commodities=847950',
            timeout=15
        )
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        text = raw_content.decode('utf-8', errors='replace')
        normalized = {
            'source_native_id': 'hmrc_847950_traders',
            'commodity_code': '847950',
            'content_type': 'html',
            'content_length': len(raw_content),
            'note': 'HMRC trader search page for HS 847950 stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, '847950_traders',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    HmrcTraderCollector().run()
