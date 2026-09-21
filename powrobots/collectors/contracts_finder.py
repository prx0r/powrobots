"""Contracts Finder / Find a Tender Collector — UK government procurement.

Uses the Contracts Finder API (OCDS format).
Source: https://www.contractsfinder.service.gov.uk/
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation, get_db

SEARCH_TERMS = [
    'robot', 'robotics', 'automation', 'automated', 'autonomous',
    'AMR', 'AGV', 'cobot', 'manipulator', 'machine vision',
    'industrial automation', 'warehouse automation',
]


class ContractsFinderCollector(BaseCollector):
    SOURCE_ID = 'contracts_finder'
    DATASET = 'procurement_notices'
    PARSER_ID = 'cf_api_v1'

    def fetch(self):
        """Search Contracts Finder for robotics-related notices."""
        all_notices = []
        for term in SEARCH_TERMS[:3]:  # Limit for initial run
            url = f'https://www.contractsfinder.service.gov.uk/Search/Results?searchTerm={term}&isMainSearch=true'
            acq = self._fetch_url(url, timeout=15)
            if acq and acq.get('status') == 200:
                all_notices.append({
                    'term': term,
                    'content_length': len(acq['content']),
                    'sha256': acq['sha256'],
                    'acquisition_id': acq['acquisition_id'],
                })
        if not all_notices:
            return None
        return json.dumps(all_notices).encode()

    def parse(self, raw_content, raw_hash, result):
        """Parse Contracts Finder results."""
        if not raw_content:
            return
        notices = json.loads(raw_content)
        for notice in notices:
            normalized = {
                'source_native_id': f"cf_{notice['term']}",
                'search_term': notice['term'],
                'content_length': notice['content_length'],
                'note': 'Contracts Finder search result stored as evidence',
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, f"cf_{notice['term']}",
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1


if __name__ == '__main__':
    ContractsFinderCollector().run()
