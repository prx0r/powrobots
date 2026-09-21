"""HMRC UK Trade Statistics Collector — robotics trade flows.

Scrapes the HMRC UK Trade Info website for trade data.
Source: https://www.uktradeinfo.com/
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record


class HmrcTradeCollector(BaseCollector):
    SOURCE_ID = 'hmrc_trade'
    DATASET = 'uk_overseas_trade'
    PARSER_ID = 'hmrc_tradeinfo_v1'

    def fetch(self):
        """Fetch HMRC trade statistics page."""
        acq = self._fetch_url('https://www.uktradeinfo.com/trade-statistics/', timeout=30)
        if acq and acq.get('status') == 200:
            return acq['content']
        # Try alternative
        acq = self._fetch_url('https://www.uktradeinfo.com/', timeout=30)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        text = raw_content.decode('utf-8', errors='replace')
        normalized = {
            'source_native_id': 'hmrc_trade_info_index',
            'content_type': 'html',
            'content_length': len(raw_content),
            'note': 'HMRC UK Trade Info main page stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'trade_info_index',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    HmrcTradeCollector().run()
