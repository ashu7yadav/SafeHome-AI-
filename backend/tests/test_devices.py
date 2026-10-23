def test_device_crud_lifecycle(client, auth_headers):
    # 1. Create a light device
    create_payload = {
        "name": "Dining Chandelier",
        "device_type": "smart_light",
        "room": "Dining Room",
        "is_online": True,
        "is_enabled": True,
        "configuration": {"brightness": 70}
    }
    create_resp = client.post("/api/devices", json=create_payload, headers=auth_headers)
    assert create_resp.status_code == 201
    device_data = create_resp.json()
    device_id = device_data["id"]
    assert device_data["name"] == "Dining Chandelier"
    assert device_data["configuration"]["brightness"] == 70

    # 2. Get device
    get_resp = client.get(f"/api/devices/{device_id}", headers=auth_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == device_id

    # 3. Update brightness
    bright_resp = client.patch(
        f"/api/devices/{device_id}/brightness",
        json={"brightness": 95},
        headers=auth_headers
    )
    assert bright_resp.status_code == 200
    assert bright_resp.json()["configuration"]["brightness"] == 95

    # 4. Brightness out of bounds validation (0-100)
    invalid_resp = client.patch(
        f"/api/devices/{device_id}/brightness",
        json={"brightness": 120},
        headers=auth_headers
    )
    assert invalid_resp.status_code == 422  # Pydantic validation error

    # 5. Toggle power
    power_resp = client.patch(
        f"/api/devices/{device_id}/power",
        json={"is_enabled": False},
        headers=auth_headers
    )
    assert power_resp.status_code == 200
    assert power_resp.json()["is_enabled"] is False

    # 6. Delete device
    del_resp = client.delete(f"/api/devices/{device_id}", headers=auth_headers)
    assert del_resp.status_code == 204

    # 7. Verify deletion
    verify_resp = client.get(f"/api/devices/{device_id}", headers=auth_headers)
    assert verify_resp.status_code == 404


def test_thermostat_and_blinds_actions(client, auth_headers):
    # Create thermostat
    t_create = client.post("/api/devices", json={
        "name": "Hallway Thermostat",
        "device_type": "thermostat",
        "room": "Hallway",
        "configuration": {"target_temperature": 70}
    }, headers=auth_headers)
    assert t_create.status_code == 201
    t_id = t_create.json()["id"]

    # Set valid temperature
    t_update = client.patch(
        f"/api/devices/{t_id}/temperature",
        json={"temperature": 72, "mode": "cool"},
        headers=auth_headers
    )
    assert t_update.status_code == 200
    assert t_update.json()["configuration"]["target_temperature"] == 72
    assert t_update.json()["configuration"]["mode"] == "cool"

    # Create blinds
    b_create = client.post("/api/devices", json={
        "name": "Study Blinds",
        "device_type": "smart_blinds",
        "room": "Study",
        "configuration": {"opening_percentage": 50}
    }, headers=auth_headers)
    assert b_create.status_code == 201
    b_id = b_create.json()["id"]

    # Set blinds opening percentage
    b_update = client.patch(
        f"/api/devices/{b_id}/blinds",
        json={"opening_percentage": 100},
        headers=auth_headers
    )
    assert b_update.status_code == 200
    assert b_update.json()["configuration"]["opening_percentage"] == 100
    assert b_update.json()["status"] == "open"
