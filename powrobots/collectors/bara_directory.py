"""BARA / Automate UK Integrator Directory Collector.

Scrapes the Automate UK / BARA product finder for UK robot integrators.
Source: https://www.automate.org.uk/
"""

import json
import re
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation, get_db


class BaraDirectoryCollector(BaseCollector):
    SOURCE_ID = 'bara_directory'
    DATASET = 'integrators'
    PARSER_ID = 'bara_web_v1'

    def fetch(self):
        """Fetch Automate UK member directory."""
        url = 'https://www.automate.org.uk/member-directory'
        acq = self._fetch_url(url, timeout=15)
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        """Parse BARA member directory."""
        if not raw_content:
            return
        html = raw_content.decode('utf-8', errors='replace')
        normalized = {
            'source_native_id': 'bara_member_directory',
            'content_type': 'html',
            'content_length': len(raw_content),
            'note': 'BARA/Automate UK member directory stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'bara_directory',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    BaraDirectoryCollector().run()
