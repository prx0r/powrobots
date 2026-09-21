"""Companies House Collector — UK company data for identified organisations.

Uses the official Companies House REST API.
Requires API key (free, register at developer.company-information.service.gov.uk).
"""

import json
import os
from datetime import datetime, timezone
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation


class CompaniesHouseCollector(BaseCollector):
    SOURCE_ID = 'companies_house'
    DATASET = 'companies'
    PARSER_ID = 'ch_api_v1'

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('CH_API_KEY', '')

    def fetch(self):
        if not self.api_key:
            return None
        # Fetch would search for robotics-related companies
        # For now, return None until API key is available
        return None

    def parse(self, raw_content, raw_hash, result):
        if not raw_content:
            return
        data = json.loads(raw_content)
        for company in data.get('items', []):
            company_number = company.get('company_number', '')
            name = company.get('title', '')
            if not company_number or not name:
                result.records_invalid += 1
                continue

            normalized = {
                'source_native_id': company_number,
                'company_number': company_number,
                'name': name,
                'status': company.get('company_status', ''),
                'type': company.get('company_type', ''),
                'address': company.get('address', {}),
            }

            ir = insert_source_record(
                self.SOURCE_ID, self.DATASET, company_number,
                normalized, raw_hash, self.PARSER_ID, self.PARSER_VERSION
            )
            if ir['inserted']:
                if ir.get('duplicate_of'):
                    result.records_changed += 1
                else:
                    result.records_new += 1
            else:
                result.records_unchanged += 1

            upsert_organisation(
                company_number, name,
                company_number=company_number,
                org_type=company.get('company_type', '')
            )


if __name__ == '__main__':
    CompaniesHouseCollector().run()
