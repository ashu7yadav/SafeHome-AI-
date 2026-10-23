def test_security_event_lifecycle(client, auth_headers):
    # 1. Trigger demo security event
    demo_resp = client.post("/api/security/events/demo", json={
        "event_type": "motion_detection",
        "location": "Front Porch"
    }, headers=auth_headers)
    assert demo_resp.status_code == 201
    event_data = demo_resp.json()
    event_id = event_data["id"]
    assert event_data["is_acknowledged"] is False
    assert "Front Porch" in event_data["title"]

    # 2. List events with unacknowledged filter
    list_resp = client.get("/api/security/events?is_acknowledged=false", headers=auth_headers)
    assert list_resp.status_code == 200
    events = list_resp.json()
    assert any(e["id"] == event_id for e in events)

    # 3. Acknowledge alert
    ack_resp = client.patch(f"/api/security/events/{event_id}/acknowledge", headers=auth_headers)
    assert ack_resp.status_code == 200
    assert ack_resp.json()["is_acknowledged"] is True
    assert ack_resp.json()["acknowledged_by"] is not None

    # 4. Check security status reflects resolved alerts
    status_resp = client.get("/api/security/status", headers=auth_headers)
    assert status_resp.status_code == 200
    assert status_resp.json()["is_secure"] is True
    assert status_resp.json()["active_alerts_count"] == 0
