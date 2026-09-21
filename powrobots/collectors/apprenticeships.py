"""Apprenticeships Collector — UK skills demand signals.

Fetches apprenticeship listings from the Find an Apprenticeship API.
Source: https://www.gov.uk/apply-apprenticeship
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, get_db

SEARCH_TERMS = [
    'mechatronics', 'robotics', 'automation', 'PLC',
    'maintenance', 'controls', 'servo',
]


class ApprenticeshipCollector(BaseCollector):
    SOURCE_ID = 'find_apprenticeship'
    DATASET = 'apprenticeships'
    PARSER_ID = 'faa_api_v1'

    def fetch(self):
        """Search for robotics-related apprenticeships."""
        all_listings = []
        for term in SEARCH_TERMS[:3]:
            url = f'https://www.gov.uk/api/apprenticeship-vacancies?query={term}&resultsPerPage=25'
            acq = self._fetch_url(url, timeout=15)
            if acq and acq.get('status') == 200:
                try:
                    data = json.loads(acq['content'])
                    vacancies = data.get('vacancies', [])
                    for v in vacancies:
                        all_listings.append({
                            'id': v.get('id', ''),
                            'title': v.get('title', ''),
                            'employer': v.get('employer', {}).get('name', ''),
                            'location': v.get('location', {}).get('name', ''),
                            'salary': v.get('salary', ''),
                            'closing_date': v.get('closing_date', ''),
                            'search_term': term,
                        })
                except (json.JSONDecodeError, KeyError):
                    pass
        if not all_listings:
            return None
        return json.dumps(all_listings).encode()

    def parse(self, raw_content, raw_hash, result):
        """Parse apprenticeship listings."""
        if not raw_content:
            return
        listings = json.loads(raw_content)
        for listing in listings:
            listing_id = listing.get('id', '')
            if not listing_id:
                result.records_invalid += 1
                continue
            normalized = {
                'source_native_id': listing_id,
                'title': listing.get('title', ''),
                'employer': listing.get('employer', ''),
                'location': listing.get('location', ''),
                'salary': listing.get('salary', ''),
                'closing_date': listing.get('closing_date', ''),
                'search_term': listing.get('search_term', ''),
            }
            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, listing_id,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                result.records_new += 1
            else:
                result.records_unchanged += 1


if __name__ == '__main__':
    ApprenticeshipCollector().run()
