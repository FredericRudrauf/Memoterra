# backend/schemas.py
from pydantic import BaseModel
from typing import Optional

class EventBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    description: Optional[str] = None
    protagonistes: Optional[str] = None
    date_text: str

class EventCreate(EventBase):
    id_type: int
    id_era: int
    id_continent: int

class Event(EventBase):
    id: int
    type: str
    era: str
    continent: str
    image_url: Optional[str] = None  # Champ optionnel pour l'image
    video_url: Optional[str]  = None # Champ optionnel pour la vidéo
    source_url: Optional[str] = None  # Champ optionnel pour reférence supplémentaire

    class Config:
        from_attributes = True
