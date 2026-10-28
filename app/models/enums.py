import enum

class MemberRole(str, enum.Enum):
    admin = "admin"
    employee = "employee"
    guest = "guest"

class DeviceStatus(str, enum.Enum):
    online = "online"
    offline = "offline"

class AccessStatus(str, enum.Enum):
    success = "success"
    denied = "denied"