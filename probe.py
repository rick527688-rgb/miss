import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def main():
    author_id = os.environ.get('AUTHOR_ID', '').strip()
    if not author_id.isdecimal():
        print('ERROR: AUTHOR_ID must be a numeric tag ID.')
        return 2
    url = 'https://nhentai.net/api/v2/galleries/tagged?' + urllib.parse.urlencode({'tag_id': author_id, 'sort': 'date', 'page': 1})
    req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (compatible; PersonalFeedProbe/1.0)'})
    result = {'tested_at': datetime.now(timezone.utc).isoformat(), 'author_id': author_id, 'status': None, 'valid_json': False, 'item_count': None, 'error': None}
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result['status'] = response.status
            body = response.read(2_000_000)
            payload = json.loads(body)
            data = payload.get('data', payload) if isinstance(payload, dict) else payload
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = next((data[k] for k in ('result', 'galleries', 'results', 'items') if isinstance(data.get(k), list)), None)
            else:
                items = None
            result['valid_json'] = True
            if items is None:
                result['error'] = 'Unrecognized list schema'
            else:
                result['item_count'] = len(items)
    except urllib.error.HTTPError as e:
        result['status'] = e.code
        result['error'] = f'HTTP {e.code}; Retry-After={e.headers.get("Retry-After", "not supplied")}'
    except Exception as e:
        result['error'] = f'{type(e).__name__}: {e}'
    Path('probe-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 200 and result['item_count'] is not None else 1


if __name__ == '__main__':
    sys.exit(main())
