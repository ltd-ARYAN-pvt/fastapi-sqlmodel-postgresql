from datetime import datetime, timezone
from sqlmodel import Field

def utc_now():
    return datetime.now(timezone.utc)

class TimestampMixin:
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)