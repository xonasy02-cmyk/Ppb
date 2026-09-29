"""Public API regression tests: config, bag index, detail routes, launch gate, drafts, uploads."""

import io
import json
import uuid


def _draft_payload(suffix: str, image_id: str | None = None):
    token_suffix = ''.join(ch for ch in suffix.upper() if ch.isalnum())[:4] or 'T001'
    return {
        'name': f'TEST Paperbag {suffix}',
        'ticker': f'TEST{token_suffix}',
        'description': 'TEST draft for persistent flow verification.',
        'image_id': image_id,
        'website': 'https://example.com',
        'twitter': 'https://x.com/example',
        'telegram': 'https://t.me/example',
        'target_sol': 12.5,
        'asset': 'DOGE',
        'global_asset': 'USDC',
        'mode': 'SHARE',
    }


def test_health_and_config_flags(api_client, api_url):
    health = api_client.get(f'{api_url}/')
    assert health.status_code == 200
    config = api_client.get(f'{api_url}/config')
    assert config.status_code == 200
    data = config.json()
    assert data['live_transactions'] is False and data['wallet_enabled'] is False


def test_projects_support_search_and_six_seeded(api_client, api_url):
    response = api_client.get(f'{api_url}/projects', params={'sort': 'trending'})
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 6 and rows[0]['data_mode'] == 'illustrative'


def test_projects_search_matches_ticker_name_asset(api_client, api_url):
    ticker = api_client.get(f'{api_url}/projects', params={'search': 'DOG', 'sort': 'trending'})
    assert ticker.status_code == 200 and any(p['ticker'] == 'DOG' for p in ticker.json())

    by_name = api_client.get(f'{api_url}/projects', params={'search': 'Paper Cat', 'sort': 'trending'})
    assert by_name.status_code == 200 and any(p['id'] == 'cat' for p in by_name.json())

    by_asset = api_client.get(f'{api_url}/projects', params={'search': 'BONK', 'sort': 'trending'})
    assert by_asset.status_code == 200 and any(p['id'] == 'bonk' for p in by_asset.json())


def test_projects_invalid_sort_returns_422(api_client, api_url):
    response = api_client.get(f'{api_url}/projects', params={'sort': 'invalid'})
    assert response.status_code == 422


def test_project_detail_and_missing_id(api_client, api_url):
    ok = api_client.get(f'{api_url}/projects/dog')
    assert ok.status_code == 200 and ok.json()['id'] == 'dog'

    missing = api_client.get(f'{api_url}/projects/missing-id')
    assert missing.status_code == 404 and 'not found' in missing.text.lower()


def test_global_and_native_constraints(api_client, api_url):
    global_res = api_client.get(f'{api_url}/global')
    assert global_res.status_code == 200
    g = global_res.json()
    assert g['interval_hours'] == 24 and 'not live' in g['status'].lower()

    native = api_client.get(f'{api_url}/native')
    assert native.status_code == 200
    n = native.json()
    assert n['launched'] is False and n['configurable'] is False and n['mechanism'][1].startswith('80%')


def test_leaderboard_categories_and_invalid(api_client, api_url):
    for category in ['opened', 'biggest', 'fastest', 'profits', 'active']:
        response = api_client.get(f'{api_url}/leaderboard', params={'category': category})
        assert response.status_code == 200 and len(response.json()) == 5

    invalid = api_client.get(f'{api_url}/leaderboard', params={'category': 'bad'})
    assert invalid.status_code == 422


def test_forbidden_fee_breakdown_not_exposed(api_client, api_url):
    targets = [
        api_client.get(f'{api_url}/config').json(),
        api_client.get(f'{api_url}/overview').json(),
        api_client.get(f'{api_url}/global').json(),
        api_client.get(f'{api_url}/native').json(),
    ]
    raw = json.dumps(targets).lower()
    assert '0.4%' not in raw and '0.2%' not in raw and 'creator fee' not in raw


def test_launch_locked_503(api_client, api_url):
    response = api_client.post(f'{api_url}/launch')
    assert response.status_code == 503 and 'not configured' in response.text.lower()


def test_upload_rejects_invalid_mime(api_client, api_url):
    fake_text = io.BytesIO(b'not an image')
    response = api_client.post(
        f'{api_url}/uploads',
        files={'file': ('bad.txt', fake_text, 'text/plain')},
    )
    assert response.status_code == 415


def test_upload_accepts_real_png_and_is_fetchable(api_client, api_url):
    # 1x1 transparent PNG
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\x0cIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    response = api_client.post(
        f'{api_url}/uploads',
        files={'file': ('tiny.png', io.BytesIO(png_bytes), 'image/png')},
    )
    assert response.status_code == 201
    file_id = response.json()['id']
    get_file = api_client.get(f'{api_url}/files/{file_id}')
    assert get_file.status_code == 200 and get_file.headers['content-type'].startswith('image/png')


def test_missing_file_returns_404(api_client, api_url):
    response = api_client.get(f'{api_url}/files/{uuid.uuid4()}')
    assert response.status_code == 404


def test_create_get_update_delete_draft_persistence(api_client, api_url):
    suffix = str(uuid.uuid4())[:6]
    payload = _draft_payload(suffix)

    created = api_client.post(f'{api_url}/drafts', json=payload)
    assert created.status_code == 201
    draft_id = created.json()['id']

    fetched = api_client.get(f'{api_url}/drafts/{draft_id}')
    assert fetched.status_code == 200 and fetched.json()['trading_pair'] == f"{payload['ticker']}/SOL"

    updated_payload = payload | {'mode': 'BURN', 'global_asset': 'BONK'}
    updated = api_client.put(f'{api_url}/drafts/{draft_id}', json=updated_payload)
    assert updated.status_code == 200 and updated.json()['mode'] == 'BURN'

    refetched = api_client.get(f'{api_url}/drafts/{draft_id}')
    assert refetched.status_code == 200 and refetched.json()['global_asset'] == 'BONK'

    deleted = api_client.delete(f'{api_url}/drafts/{draft_id}')
    assert deleted.status_code == 204

    missing = api_client.get(f'{api_url}/drafts/{draft_id}')
    assert missing.status_code == 404


def test_draft_validation_rejects_bad_ticker_and_bad_https(api_client, api_url):
    payload = _draft_payload('BAD1')
    payload['ticker'] = 'bad'
    bad_ticker = api_client.post(f'{api_url}/drafts', json=payload)
    assert bad_ticker.status_code == 422

    payload = _draft_payload('BAD2')
    payload['website'] = 'http://insecure.com'
    bad_link = api_client.post(f'{api_url}/drafts', json=payload)
    assert bad_link.status_code == 422


def test_draft_validation_rejects_non_positive_or_non_finite(api_client, api_url):
    payload = _draft_payload('NUM1')
    payload['target_sol'] = 0
    zero = api_client.post(f'{api_url}/drafts', json=payload)
    assert zero.status_code == 422

    payload = _draft_payload('NUM2')
    payload['target_sol'] = 1000001
    over_max = api_client.post(f'{api_url}/drafts', json=payload)
    assert over_max.status_code == 422

    payload = _draft_payload('NUM3')
    payload['target_sol'] = 'inf'
    non_finite = api_client.post(f'{api_url}/drafts', json=payload)
    assert non_finite.status_code == 422


def test_missing_draft_returns_404(api_client, api_url):
    response = api_client.get(f'{api_url}/drafts/{uuid.uuid4()}')
    assert response.status_code == 404
