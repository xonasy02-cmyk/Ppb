"""Market/trading regression tests: chart fixtures and simulated buy/sell workflow."""

import uuid


def test_project_has_required_market_fields(api_client, api_url):
    response = api_client.get(f"{api_url}/projects/dog")
    assert response.status_code == 200
    data = response.json()
    required = [
        "price_usd",
        "price_sol",
        "market_cap",
        "volume",
        "liquidity",
        "holders",
        "change_24h",
    ]
    assert all(key in data for key in required)


def test_market_candles_support_all_timeframes(api_client, api_url):
    for timeframe in ["1m", "5m", "15m", "1h", "4h"]:
        response = api_client.get(f"{api_url}/market/dog/candles", params={"timeframe": timeframe})
        assert response.status_code == 200
        payload = response.json()
        assert payload["timeframe"] == timeframe
        assert payload["data_mode"] == "illustrative"
        assert len(payload["candles"]) > 0


def test_market_candles_invalid_timeframe_422(api_client, api_url):
    response = api_client.get(f"{api_url}/market/dog/candles", params={"timeframe": "10m"})
    assert response.status_code == 422


def test_market_trades_and_holders_sample_marked(api_client, api_url):
    trades = api_client.get(f"{api_url}/market/dog/trades")
    assert trades.status_code == 200
    t_data = trades.json()
    assert t_data["data_mode"] == "illustrative" and len(t_data["items"]) == 24

    holders = api_client.get(f"{api_url}/market/dog/holders")
    assert holders.status_code == 200
    h_data = holders.json()
    assert h_data["data_mode"] == "illustrative" and h_data["total"] > 0 and len(h_data["items"]) == 10


def test_market_unknown_project_returns_404(api_client, api_url):
    response = api_client.get(f"{api_url}/market/unknown-token/candles")
    assert response.status_code == 404


def test_simulation_create_buy_sell_and_delete_flow(api_client, api_url):
    created = api_client.post(f"{api_url}/simulations")
    assert created.status_code == 201
    simulation = created.json()
    sim_id = simulation["id"]
    assert simulation["balance_sol"] == 100

    buy_request_id = str(uuid.uuid4())
    buy = api_client.post(
        f"{api_url}/simulations/{sim_id}/orders",
        json={"project_id": "dog", "side": "buy", "amount": 1, "request_id": buy_request_id},
    )
    assert buy.status_code == 200
    buy_data = buy.json()
    assert buy_data["trade"]["side"] == "buy"
    assert buy_data["simulation"]["balance_sol"] == 99

    quantity = buy_data["trade"]["quantity"]
    sell = api_client.post(
        f"{api_url}/simulations/{sim_id}/orders",
        json={"project_id": "dog", "side": "sell", "amount": quantity, "request_id": str(uuid.uuid4())},
    )
    assert sell.status_code == 200
    assert sell.json()["trade"]["side"] == "sell"

    remove = api_client.delete(f"{api_url}/simulations/{sim_id}")
    assert remove.status_code == 204

    missing = api_client.get(f"{api_url}/simulations/{sim_id}")
    assert missing.status_code == 404


def test_simulation_idempotency_and_payload_mismatch(api_client, api_url):
    created = api_client.post(f"{api_url}/simulations")
    assert created.status_code == 201
    sim_id = created.json()["id"]

    try:
        request_id = str(uuid.uuid4())
        first = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "dog", "side": "buy", "amount": 1, "request_id": request_id},
        )
        assert first.status_code == 200
        first_trade_id = first.json()["trade"]["id"]

        duplicate_same = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "dog", "side": "buy", "amount": 1, "request_id": request_id},
        )
        assert duplicate_same.status_code == 200
        assert duplicate_same.json()["trade"]["id"] == first_trade_id

        duplicate_changed = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "dog", "side": "buy", "amount": 2, "request_id": request_id},
        )
        assert duplicate_changed.status_code == 409
    finally:
        api_client.delete(f"{api_url}/simulations/{sim_id}")


def test_simulation_validation_and_guardrails(api_client, api_url):
    created = api_client.post(f"{api_url}/simulations")
    assert created.status_code == 201
    sim_id = created.json()["id"]

    try:
        bad_side = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "dog", "side": "hold", "amount": 1, "request_id": str(uuid.uuid4())},
        )
        assert bad_side.status_code == 422

        invalid_project = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "unknown", "side": "buy", "amount": 1, "request_id": str(uuid.uuid4())},
        )
        assert invalid_project.status_code == 404

        zero_amount = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "dog", "side": "buy", "amount": 0, "request_id": str(uuid.uuid4())},
        )
        assert zero_amount.status_code == 422

        insufficient_sol = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "dog", "side": "buy", "amount": 1000, "request_id": str(uuid.uuid4())},
        )
        assert insufficient_sol.status_code == 422

        oversell = api_client.post(
            f"{api_url}/simulations/{sim_id}/orders",
            json={"project_id": "dog", "side": "sell", "amount": 1, "request_id": str(uuid.uuid4())},
        )
        assert oversell.status_code == 422
    finally:
        api_client.delete(f"{api_url}/simulations/{sim_id}")
