import json
import uuid
from datetime import datetime, timedelta, timezone
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.device import Device
from app.models.security_event import SecurityEvent
from app.models.visitor import Visitor
from app.models.automation import Automation
from app.models.notification import Notification

DEMO_HOUSEHOLD_ID = "00000000-0000-0000-0000-000000000001"
DEMO_USER_EMAIL = "alex@safehome.ai"


def seed_database():
    print("[SEED] Initializing SafeHome AI database tables...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Create or get Demo User
        user = db.query(User).filter(User.email == DEMO_USER_EMAIL).first()
        if not user:
            print("Creating demo homeowner account: alex@safehome.ai")
            user = User(
                id="00000000-0000-0000-0000-000000000010",
                household_id=DEMO_HOUSEHOLD_ID,
                full_name="Alex Morgan",
                email=DEMO_USER_EMAIL,
                password_hash=get_password_hash("SafeHome123!"),
                role="homeowner",
                is_active=True,
                created_at=datetime.now(timezone.utc)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            print("Demo user alex@safehome.ai already exists.")

        # 2. Seed Devices
        seed_devices = [
            # 4 Cameras (3 online, 1 offline) -> CCTV 3/4 online
            {
                "id": "cam-pet-01",
                "name": "Pet cam",
                "device_type": "security_camera",
                "room": "Dining Room CCTV",
                "is_online": True,
                "is_enabled": True,
                "status": "online",
                "configuration": {
                    "image_url": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=85",
                    "stream_resolution": "FHD",
                    "fps": 30
                }
            },
            {
                "id": "cam-doorbell-02",
                "name": "Smart Doorbell",
                "device_type": "security_camera",
                "room": "Living Room CCTV",
                "is_online": True,
                "is_enabled": True,
                "status": "online",
                "configuration": {
                    "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=85",
                    "stream_resolution": "FHD",
                    "fps": 30
                }
            },
            {
                "id": "cam-yard-03",
                "name": "Yard cam",
                "device_type": "security_camera",
                "room": "Living Room CCTV",
                "is_online": True,
                "is_enabled": True,
                "status": "online",
                "configuration": {
                    "image_url": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea?auto=format&fit=crop&w=1600&q=85",
                    "stream_resolution": "FHD",
                    "fps": 30
                }
            },
            {
                "id": "cam-driveway-04",
                "name": "Driveway Camera",
                "device_type": "security_camera",
                "room": "Outdoor Driveway",
                "is_online": False,
                "is_enabled": False,
                "status": "offline",
                "configuration": {
                    "stream_resolution": "720p",
                    "fps": 0
                }
            },

            # 6 Smart Lights -> Lighting 6 lights
            {
                "id": "light-pantry-01",
                "name": "Pantry light",
                "device_type": "smart_light",
                "room": "Living Room",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {
                    "brightness": 84,
                    "color_temp": "warm"
                }
            },
            {
                "id": "light-kitchen-02",
                "name": "Kitchen Island Pendants",
                "device_type": "smart_light",
                "room": "Kitchen",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {"brightness": 90}
            },
            {
                "id": "light-master-03",
                "name": "Master Bedroom Dimmer",
                "device_type": "smart_light",
                "room": "Master Bedroom",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {"brightness": 60}
            },
            {
                "id": "light-porch-04",
                "name": "Porch Sconces",
                "device_type": "smart_light",
                "room": "Front Porch",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {"brightness": 100}
            },
            {
                "id": "light-hallway-05",
                "name": "Hallway Accent",
                "device_type": "smart_light",
                "room": "Hallway",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {"brightness": 75}
            },
            {
                "id": "light-backyard-06",
                "name": "Backyard Floodlight",
                "device_type": "smart_light",
                "room": "Backyard",
                "is_online": True,
                "is_enabled": False,
                "status": "standby",
                "configuration": {"brightness": 0}
            },

            # 3 Speakers -> Speaker 3 devices
            {
                "id": "speaker-lr-01",
                "name": "Living Room Soundbar",
                "device_type": "speaker",
                "room": "Living Room",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {"volume": 45}
            },
            {
                "id": "speaker-kitchen-02",
                "name": "Kitchen Speaker",
                "device_type": "speaker",
                "room": "Kitchen",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {"volume": 30}
            },
            {
                "id": "speaker-patio-03",
                "name": "Patio Audio",
                "device_type": "speaker",
                "room": "Patio",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {"volume": 50}
            },

            # 2 Wi-Fi Devices -> Wi-Fi 2 devices
            {
                "id": "wifi-main-01",
                "name": "SafeHome Mesh Router",
                "device_type": "wifi_device",
                "room": "Hallway",
                "is_online": True,
                "is_enabled": True,
                "status": "online",
                "configuration": {"ip": "192.168.1.1", "channel": "5GHz"}
            },
            {
                "id": "wifi-extender-02",
                "name": "Upstairs Range Extender",
                "device_type": "wifi_device",
                "room": "Upstairs",
                "is_online": True,
                "is_enabled": True,
                "status": "online",
                "configuration": {"signal_dbm": -48}
            },

            # 4 Smart Assistants -> Assistant 4 devices
            {
                "id": "asst-lr-01",
                "name": "Living Room Hub",
                "device_type": "smart_assistant",
                "room": "Living Room",
                "is_online": True,
                "is_enabled": True,
                "status": "listening",
                "configuration": {"mic_muted": False}
            },
            {
                "id": "asst-kitchen-02",
                "name": "Kitchen Display",
                "device_type": "smart_assistant",
                "room": "Kitchen",
                "is_online": True,
                "is_enabled": True,
                "status": "listening",
                "configuration": {"mic_muted": False}
            },
            {
                "id": "asst-bed-03",
                "name": "Bedroom Assistant",
                "device_type": "smart_assistant",
                "room": "Master Bedroom",
                "is_online": True,
                "is_enabled": True,
                "status": "listening",
                "configuration": {"mic_muted": False}
            },
            {
                "id": "asst-study-04",
                "name": "Study Speaker",
                "device_type": "smart_assistant",
                "room": "Study",
                "is_online": True,
                "is_enabled": True,
                "status": "listening",
                "configuration": {"mic_muted": False}
            },

            # Primary Favorite Controls
            {
                "id": "thermostat-hallway-01",
                "name": "Hallway thermostat",
                "device_type": "thermostat",
                "room": "Hallway",
                "is_online": True,
                "is_enabled": True,
                "status": "active",
                "configuration": {
                    "target_temperature": 70.0,
                    "ambient_temperature": 70.4,
                    "mode": "heat"
                }
            },
            {
                "id": "lock-front-01",
                "name": "Front door lock",
                "device_type": "door_lock",
                "room": "Front entrance",
                "is_online": True,
                "is_enabled": True,
                "status": "locked",
                "configuration": {
                    "is_locked": True,
                    "auto_relock_seconds": 45
                }
            },
            {
                "id": "blinds-lr-01",
                "name": "Living room blinds",
                "device_type": "smart_blinds",
                "room": "Living Room",
                "is_online": True,
                "is_enabled": True,
                "status": "open",
                "configuration": {
                    "opening_percentage": 100
                }
            },
            {
                "id": "vacuum-01",
                "name": "Smart Vacuum",
                "device_type": "smart_vacuum",
                "room": "Ground Floor",
                "is_online": True,
                "is_enabled": True,
                "status": "running",
                "configuration": {
                    "is_running": True,
                    "progress": 46,
                    "battery": 82
                }
            }
        ]

        for dev_data in seed_devices:
            existing_dev = db.query(Device).filter(Device.id == dev_data["id"]).first()
            if not existing_dev:
                dev = Device(
                    id=dev_data["id"],
                    household_id=DEMO_HOUSEHOLD_ID,
                    name=dev_data["name"],
                    device_type=dev_data["device_type"],
                    room=dev_data["room"],
                    is_online=dev_data["is_online"],
                    is_enabled=dev_data["is_enabled"],
                    status=dev_data["status"],
                    configuration_json=json.dumps(dev_data["configuration"]),
                    last_seen=datetime.now(timezone.utc),
                    created_at=datetime.now(timezone.utc)
                )
                db.add(dev)
        db.commit()
        print("Devices seeded successfully.")

        # 3. Seed Security Events
        seed_events = [
            {
                "id": "event-01",
                "device_id": "cam-doorbell-02",
                "event_type": "motion_detection",
                "severity": "warning",
                "title": "Motion detected at Front Porch",
                "description": "Smart Doorbell camera detected motion at front walkway.",
                "source": "simulated",
                "is_acknowledged": False,
                "created_at": datetime.now(timezone.utc) - timedelta(minutes=2)
            },
            {
                "id": "event-02",
                "device_id": "light-pantry-01",
                "event_type": "system_status",
                "severity": "informational",
                "title": "Pantry light brightness adjusted to 84%",
                "description": "Adaptive lighting routine applied to Living Room.",
                "source": "simulated",
                "is_acknowledged": True,
                "created_at": datetime.now(timezone.utc) - timedelta(minutes=18)
            },
            {
                "id": "event-03",
                "device_id": "vacuum-01",
                "event_type": "system_status",
                "severity": "informational",
                "title": "Smart vacuum started scheduled clean",
                "description": "RoboVac 900 undocked and initiated daily living area vacuuming.",
                "source": "simulated",
                "is_acknowledged": True,
                "created_at": datetime.now(timezone.utc) - timedelta(minutes=42)
            },
            {
                "id": "event-04",
                "device_id": "lock-front-01",
                "event_type": "door_access",
                "severity": "informational",
                "title": "Front door locked automatically",
                "description": "Auto-relock timer engaged following entrance closure.",
                "source": "simulated",
                "is_acknowledged": True,
                "created_at": datetime.now(timezone.utc) - timedelta(hours=1)
            }
        ]

        for ev in seed_events:
            existing_event = db.query(SecurityEvent).filter(SecurityEvent.id == ev["id"]).first()
            if not existing_event:
                event_obj = SecurityEvent(
                    id=ev["id"],
                    household_id=DEMO_HOUSEHOLD_ID,
                    device_id=ev["device_id"],
                    event_type=ev["event_type"],
                    severity=ev["severity"],
                    title=ev["title"],
                    description=ev["description"],
                    source=ev["source"],
                    is_acknowledged=ev["is_acknowledged"],
                    created_at=ev["created_at"],
                    acknowledged_at=ev["created_at"] if ev["is_acknowledged"] else None,
                    acknowledged_by="Alex Morgan" if ev["is_acknowledged"] else None
                )
                db.add(event_obj)
        db.commit()
        print("Security events seeded.")

        # 4. Seed Notifications
        seed_notifications = [
            {
                "id": "notif-01",
                "title": "Person detected at Front Entrance",
                "message": "Smart Doorbell · 2 minutes ago",
                "notification_type": "security_alert",
                "is_read": False,
                "related_event_id": "event-01",
                "created_at": datetime.now(timezone.utc) - timedelta(minutes=2)
            },
            {
                "id": "notif-02",
                "title": "Pantry light scheduled dimming",
                "message": "Living Room · 18 minutes ago",
                "notification_type": "routine",
                "is_read": True,
                "related_event_id": "event-02",
                "created_at": datetime.now(timezone.utc) - timedelta(minutes=18)
            }
        ]

        for n in seed_notifications:
            existing_notif = db.query(Notification).filter(Notification.id == n["id"]).first()
            if not existing_notif:
                notif_obj = Notification(
                    id=n["id"],
                    household_id=DEMO_HOUSEHOLD_ID,
                    title=n["title"],
                    message=n["message"],
                    notification_type=n["notification_type"],
                    is_read=n["is_read"],
                    related_event_id=n["related_event_id"],
                    created_at=n["created_at"]
                )
                db.add(notif_obj)
        db.commit()
        print("Notifications seeded.")

        # 5. Seed Visitors
        seed_visitors = [
            {
                "id": "vis-01",
                "visitor_name": "Jordan Rivera (Courier)",
                "contact_information": "courier-dispatch@courier.net",
                "purpose": "Package Delivery",
                "access_status": "approved",
                "valid_from": datetime.now(timezone.utc) - timedelta(hours=1),
                "valid_until": datetime.now(timezone.utc) + timedelta(hours=3),
                "approved_by": "Alex Morgan"
            },
            {
                "id": "vis-02",
                "visitor_name": "Taylor Smith (HVAC Tech)",
                "contact_information": "+1-555-0199",
                "purpose": "Thermostat Sensor Maintenance",
                "access_status": "approved",
                "valid_from": datetime.now(timezone.utc) + timedelta(days=1),
                "valid_until": datetime.now(timezone.utc) + timedelta(days=1, hours=4),
                "approved_by": "Alex Morgan"
            }
        ]

        for v in seed_visitors:
            existing_v = db.query(Visitor).filter(Visitor.id == v["id"]).first()
            if not existing_v:
                v_obj = Visitor(
                    id=v["id"],
                    household_id=DEMO_HOUSEHOLD_ID,
                    visitor_name=v["visitor_name"],
                    contact_information=v["contact_information"],
                    purpose=v["purpose"],
                    access_status=v["access_status"],
                    valid_from=v["valid_from"],
                    valid_until=v["valid_until"],
                    created_at=datetime.now(timezone.utc),
                    approved_by=v["approved_by"]
                )
                db.add(v_obj)
        db.commit()
        print("Visitors seeded.")

        # 6. Seed Automations
        seed_automations = [
            {
                "id": "auto-01",
                "name": "Movie Night Scene",
                "description": "Dims pantry lighting to 15%, shuts blinds, sets Dolby Atmos.",
                "trigger_type": "scene",
                "trigger_configuration": {"scene": "movie_mode"},
                "action_configuration": {"dim_lights": 15, "shut_blinds": True},
                "is_enabled": True
            },
            {
                "id": "auto-02",
                "name": "Away Security Shield",
                "description": "Arms all perimeter CCTV cameras and locks exterior doors.",
                "trigger_type": "geofence",
                "trigger_configuration": {"all_occupants_away": True},
                "action_configuration": {"lock_doors": True, "arm_cameras": True},
                "is_enabled": False
            },
            {
                "id": "auto-03",
                "name": "Night Owl Guard",
                "description": "Activates yard motion tripwires and turns porch downlights to amber.",
                "trigger_type": "schedule",
                "trigger_configuration": {"cron": "0 22 * * *"},
                "action_configuration": {"porch_amber": True, "arm_cameras": True},
                "is_enabled": True
            },
            {
                "id": "auto-04",
                "name": "Welcome Home Arrival",
                "description": "Disarms entrance lock, adjusts hallway climate to 70°F, resumes lights.",
                "trigger_type": "geofence",
                "trigger_configuration": {"occupant_arrived": True},
                "action_configuration": {"set_temp": 70, "unlock_door": True},
                "is_enabled": False
            }
        ]

        for a in seed_automations:
            existing_a = db.query(Automation).filter(Automation.id == a["id"]).first()
            if not existing_a:
                a_obj = Automation(
                    id=a["id"],
                    household_id=DEMO_HOUSEHOLD_ID,
                    name=a["name"],
                    description=a["description"],
                    trigger_type=a["trigger_type"],
                    trigger_configuration=json.dumps(a["trigger_configuration"]),
                    action_configuration=json.dumps(a["action_configuration"]),
                    is_enabled=a["is_enabled"],
                    created_at=datetime.now(timezone.utc)
                )
                db.add(a_obj)
        db.commit()
        print("Automations seeded.")

        print("[SUCCESS] Database successfully seeded with demo household!")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error during seed: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
