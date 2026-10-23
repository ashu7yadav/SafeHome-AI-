from datetime import datetime, timedelta, timezone


def test_visitor_management(client, auth_headers):
    # 1. Register visitor pass
    valid_until = (datetime.now(timezone.utc) + timedelta(hours=4)).isoformat()
    create_resp = client.post("/api/visitors", json={
        "visitor_name": "Sam Porter (Plumber)",
        "contact_information": "+1-555-0144",
        "purpose": "Kitchen sink repair",
        "valid_until": valid_until
    }, headers=auth_headers)
    assert create_resp.status_code == 201
    vis_data = create_resp.json()
    vis_id = vis_data["id"]
    assert vis_data["access_status"] == "approved"

    # 2. Revoke visitor pass
    revoke_resp = client.patch(f"/api/visitors/{vis_id}/revoke", headers=auth_headers)
    assert revoke_resp.status_code == 200
    assert revoke_resp.json()["access_status"] == "revoked"

    # 3. Approve visitor pass again
    approve_resp = client.patch(f"/api/visitors/{vis_id}/approve", headers=auth_headers)
    assert approve_resp.status_code == 200
    assert approve_resp.json()["access_status"] == "approved"

    # 4. List visitors
    list_resp = client.get("/api/visitors", headers=auth_headers)
    assert list_resp.status_code == 200
    assert any(v["id"] == vis_id for v in list_resp.json())

    # 5. Delete visitor
    del_resp = client.delete(f"/api/visitors/{vis_id}", headers=auth_headers)
    assert del_resp.status_code == 204
