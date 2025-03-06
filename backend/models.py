# backend/models.py
from sqlalchemy import Column, Integer, String, Float, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class Historical_Event(Base):
    __tablename__ = "historical_events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    era = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Event {self.name}>"
    