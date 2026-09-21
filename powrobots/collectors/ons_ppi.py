"""ONS PPI Collector — Producer Price Index time series.

Scrapes the ONS inflation data pages.
Source: https://www.ons.gov.uk/economy/inflationandpriceindices
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record


class OnsPpiCollector(BaseCollector):
    SOURCE_ID = 'ons_ppi'
    DATASET = 'producer_prices'
    PARSER_ID = 'ons_web_v1'

    def fetch(self):
        """Fetch ONS inflation and price indices page."""
        acq = self._fetch_url(
            'https://www.ons.gov.uk/economy/inflationandpriceindices',
            timeout=30
        )
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        normalized = {
            'source_native_id': 'ons_inflation_indices',
            'content_type': 'html',
            'content_length': len(raw_content),
            'note': 'ONS inflation and price indices page stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'inflation_indices',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    OnsPpiCollector().run()
