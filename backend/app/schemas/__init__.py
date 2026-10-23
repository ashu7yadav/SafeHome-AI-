from app.schemas.auth import UserRegister, UserLogin, Token, TokenPayload, UserResponse
from app.schemas.device import (
    DeviceCreate, 
    DeviceUpdate, 
    DevicePowerUpdate, 
    BrightnessUpdate, 
    TemperatureUpdate, 
    BlindsUpdate, 
    VacuumUpdate, 
    DeviceResponse
)
from app.schemas.event import (
    SecurityEventCreate, 
    SecurityEventDemo, 
    SecurityEventAcknowledge, 
    SecurityEventResponse
)
from app.schemas.visitor import VisitorCreate, VisitorUpdate, VisitorResponse
from app.schemas.automation import (
    AutomationCreate, 
    AutomationUpdate, 
    AutomationResponse, 
    AutomationTestResult
)
from app.schemas.notification import (
    NotificationCreate, 
    NotificationResponse, 
    UnreadCountResponse
)

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "TokenPayload",
    "UserResponse",
    "DeviceCreate",
    "DeviceUpdate",
    "DevicePowerUpdate",
    "BrightnessUpdate",
    "TemperatureUpdate",
    "BlindsUpdate",
    "VacuumUpdate",
    "DeviceResponse",
    "SecurityEventCreate",
    "SecurityEventDemo",
    "SecurityEventAcknowledge",
    "SecurityEventResponse",
    "VisitorCreate",
    "VisitorUpdate",
    "VisitorResponse",
    "AutomationCreate",
    "AutomationUpdate",
    "AutomationResponse",
    "AutomationTestResult",
    "NotificationCreate",
    "NotificationResponse",
    "UnreadCountResponse",
]
