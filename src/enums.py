from enum import StrEnum


class UserRole(StrEnum):
    MEMBER = "MEMBER"
    AGENT = "AGENT"
    ADMIN = "ADMIN"


class TicketStatus(StrEnum):
    OPEN = "OPEN",
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class TicketPriority(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"