"""Apprenticeships Collector — UK skills demand signals.

Scrapes the Find an Apprenticeship search page.
Source: https://www.gov.uk/apply-apprenticeship
"""

import json
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record


class ApprenticeshipCollector(BaseCollector):
    SOURCE_ID = 'find_apprenticeship'
    DATASET = 'apprenticeships'
    PARSER_ID = 'faa_web_v1'

    def fetch(self):
        """Fetch apprenticeship search results for robotics terms."""
        acq = self._fetch_url(
            'https://www.gov.uk/apply-apprenticeship',
            timeout=15
        )
        if acq and acq.get('status') == 200:
            return acq['content']
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        normalized = {
            'source_native_id': 'govuk_apprenticeships',
            'content_type': 'html',
            'content_length': len(raw_content),
            'note': 'GOV.UK apprenticeship search page stored as evidence',
        }
        ir = insert_source_record(
            self.SOURCE_ID, self.DATASET, 'apprenticeships_page',
            normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
        )
        if ir['inserted']:
            result.records_new += 1
        else:
            result.records_unchanged += 1


if __name__ == '__main__':
    ApprenticeshipCollector().run()
