"""Companies House Collector — UK company data for identified organisations.

Uses the official Companies House REST API.
Requires API key (free, register at developer.company-information.service.gov.uk).
"""

import base64
import json
import os
from powrobots.collectors.base import BaseCollector, CollectorResult
from powrobots.shared.persist import insert_source_record, upsert_organisation

SEARCH_TERMS = [
    'robotics', 'robot', 'automation', 'automated', 'autonomous',
    'cobot', 'AGV', 'AMR', 'machine vision', 'industrial automation',
]

API_BASE = 'https://api.company-information.service.gov.uk'


class CompaniesHouseCollector(BaseCollector):
    SOURCE_ID = 'companies_house'
    DATASET = 'companies'
    PARSER_ID = 'ch_api_v1'

    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.environ.get('COMPANIES_HOUSE_API_KEY', '')

    def fetch(self):
        """Search Companies House for robotics-related companies."""
        if not self.api_key:
            return None

        all_items = []
        for term in SEARCH_TERMS[:5]:
            url = f'{API_BASE}/search/companies?q={term}&items_per_page=50'
            auth = base64.b64encode(f'{self.api_key}:'.encode()).decode()
            acq = self._fetch_url(
                url, timeout=15,
                headers={'Authorization': f'Basic {auth}'}
            )
            if acq and acq.get('status') == 200:
                try:
                    data = json.loads(acq['content'])
                    items = data.get('items', [])
                    for item in items:
                        item['_search_term'] = term
                    all_items.extend(items)
                except (json.JSONDecodeError, KeyError):
                    pass

        if not all_items:
            return None

        # Deduplicate by company number
        seen = {}
        for item in all_items:
            cn = item.get('company_number', '')
            if cn and cn not in seen:
                seen[cn] = item

        return json.dumps(list(seen.values())).encode()

    def parse(self, raw_content, raw_hash, result):
        """Parse Companies House search results."""
        if not raw_content:
            return

        companies = json.loads(raw_content)
        for company in companies:
            company_number = company.get('company_number', '')
            name = company.get('title', '')
            if not company_number or not name:
                result.records_invalid += 1
                continue

            address = company.get('address', {})
            address_parts = [
                address.get('address_line_1', ''),
                address.get('address_line_2', ''),
                address.get('locality', ''),
                address.get('region', ''),
                address.get('postal_code', ''),
            ]
            address_str = ', '.join(p for p in address_parts if p)

            normalized = {
                'company_number': company_number,
                'name': name,
                'status': company.get('company_status', ''),
                'type': company.get('company_type', ''),
                'address': address_str,
                'locality': address.get('locality', ''),
                'region': address.get('region', ''),
                'postcode': address.get('postal_code', ''),
                'search_term': company.get('_search_term', ''),
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

            # Upsert as organisation
            org_id = f"uk_company:{company_number}"
            upsert_organisation(
                org_id=org_id,
                canonical_name=name,
                company_number=company_number,
                country_code='GB',
                region=address.get('region', ''),
                org_type=company.get('company_type', ''),
                aliases=[name],
            )


if __name__ == '__main__':
    CompaniesHouseCollector().run()
