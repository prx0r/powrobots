"""OPSS Product Safety Collector — UK safety alerts/recalls.

Scrapes the UK Office for Product Safety and Standards alerts.
Source: https://www.gov.uk/product-safety-alerts-reports-recalls
"""

import json
import re
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, get_db


class OpsSafetyCollector(BaseCollector):
    SOURCE_ID = 'opss_safety'
    DATASET = 'safety_alerts'
    PARSER_ID = 'opss_web_v1'

    def fetch(self):
        """Fetch OPSS product safety alerts."""
        url = 'https://www.gov.uk/product-safety-alerts-reports-recalls?categories%5B0%5D=machinery'
        acq = self._fetch_url(url, timeout=15)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        """Parse OPSS alerts page."""
        if not raw_content:
            return
        html = raw_content.decode('utf-8', errors='replace')
        # Extract alert entries from the page
        # Store as evidence for later structured extraction
        normalized = {
            'source_native_id': 'opss_machinery_alerts',
            'content_type': 'html',
            'content_length': len(raw_content),
            'category': 'machinery',
            'note': 'OPSS machinery safety alerts page stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'opss_machinery_page',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    OpsSafetyCollector().run()
