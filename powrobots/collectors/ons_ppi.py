"""ONS PPI Collector — Producer Price Index time series.

Downloads ONS PPI data for electronics/machinery categories.
Source: https://www.ons.gov.uk/economy/inflationandpriceindices
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record


class OnsPpiCollector(BaseCollector):
    SOURCE_ID = 'ons_ppi'
    DATASET = 'producer_prices'
    PARSER_ID = 'ons_api_v1'

    def fetch(self):
        """Fetch ONS PPI data."""
        # ONS API endpoint for time series
        url = 'https://api.ons.gov.uk/timeseries/K376/dataset/mm23/data'
        acq = self._fetch_url(url, timeout=15)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        """Parse ONS PPI data."""
        if not raw_content:
            return
        normalized = {
            'source_native_id': 'ons_ppi_index',
            'content_type': 'json',
            'content_length': len(raw_content),
            'note': 'ONS PPI data stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'ppi_index',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    OnsPpiCollector().run()
