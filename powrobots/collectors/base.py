"""Base collector for POWRobots."""

import json
import time
import requests
from datetime import datetime, timezone
from powrobots.shared.persist import (
    get_db, store_raw, store_acquisition, insert_source_record,
    log_run, check_source_rights
)


class CollectorResult:
    def __init__(self):
        self.raw_fetched = 0
        self.raw_new = 0
        self.records_new = 0
        self.records_unchanged = 0
        self.records_changed = 0
        self.records_invalid = 0
        self.errors = []
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.finished_at = None
        self.requests_attempted = 0
        self.requests_200 = 0
        self.requests_403 = 0
        self.requests_429 = 0
        self.requests_failed = 0


class BaseCollector:
    SOURCE_ID = ''
    DATASET = ''
    PARSER_ID = ''
    PARSER_VERSION = '1.0.0'

    def __init__(self):
        self.requests_attempted = 0
        self.requests_200 = 0
        self.requests_403 = 0
        self.requests_429 = 0
        self.requests_failed = 0

    def fetch(self):
        raise NotImplementedError

    def parse(self, raw_content, raw_hash, result):
        raise NotImplementedError

    def _fetch_url(self, url, max_retries=3, timeout=30, headers=None):
        merged = {'User-Agent': 'POWRobots/1.0'}
        if headers:
            merged.update(headers)
        for attempt in range(max_retries):
            try:
                self.requests_attempted += 1
                resp = requests.get(url, timeout=timeout, headers=merged)
                if resp.status_code == 200:
                    self.requests_200 += 1
                    content = resp.content
                    raw = store_raw(content, self.SOURCE_ID)
                    acq_id = store_acquisition(
                        self.SOURCE_ID, self.DATASET, url, 200,
                        raw['sha256'], resp.headers.get('content-type', ''), len(content)
                    )
                    return {'content': content, 'sha256': raw['sha256'],
                            'acquisition_id': acq_id, 'status': 200}
                if resp.status_code == 403:
                    self.requests_403 += 1
                elif resp.status_code == 429:
                    self.requests_429 += 1
                    time.sleep(min(60, 2 ** (attempt + 2)))
                    continue
                else:
                    self.requests_failed += 1
                time.sleep(2 ** attempt)
            except requests.exceptions.RequestException:
                self.requests_failed += 1
                time.sleep(2 ** attempt)
        return None

    def run(self):
        result = CollectorResult()
        print(f'{self.SOURCE_ID} — {self.DATASET}')
        print('=' * 50)
        rights = check_source_rights(self.SOURCE_ID)
        if not rights['allowed']:
            result.errors.append('rights_blocked')
            result.finished_at = datetime.now(timezone.utc).isoformat()
            log_run(self.SOURCE_ID, 'blocked', error='rights_blocked',
                    started_at=result.started_at, finished_at=result.finished_at)
            return result
        try:
            print('  Fetching...')
            raw_content = self.fetch()
            if raw_content is None:
                result.errors.append('fetch_failed')
                return result
            result.raw_fetched = 1
            raw_result = store_raw(raw_content, self.SOURCE_ID)
            raw_hash = raw_result['sha256']
            result.raw_new = 1 if raw_result['inserted'] else 0
            store_acquisition(self.SOURCE_ID, self.DATASET,
                              f'{self.SOURCE_ID}://batch', 200, raw_hash, content_length=len(raw_content))
            print(f'  Raw: {raw_hash[:12]}... ({len(raw_content):,} bytes)')
            print('  Parsing...')
            self.parse(raw_content, raw_hash, result)
            print(f'  New: {result.records_new} | Unchanged: {result.records_unchanged}')
        except Exception as e:
            result.errors.append(str(e))
            print(f'  ERROR: {e}')
        finally:
            result.finished_at = datetime.now(timezone.utc).isoformat()
            log_run(self.SOURCE_ID, 'ok' if not result.errors else 'error',
                    result.raw_fetched, result.raw_new,
                    result.records_new, result.records_unchanged, result.records_changed,
                    result.records_invalid,
                    error=json.dumps(result.errors) if result.errors else None,
                    started_at=result.started_at, finished_at=result.finished_at)
        return result
