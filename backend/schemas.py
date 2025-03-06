# backend/schemas.py
from datetime import date
from typing import Optional
from pydantic import BaseModel

class EventBase(BaseModel):
    name: str
    type: str
    latitude: float
    longitude: float
    date: Optional[date] = None
    description: Optional[str] = None
    era: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        orm_mode = True
