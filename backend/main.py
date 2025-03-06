# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from models import Historical_Event
from schemas import EventCreate, Event
import uvicorn

app = FastAPI(title="Carte Historique Interactive")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/events/", response_model=Event)
def create_event(event: EventCreate):
    """Créer un nouvel événement historique"""
    db_event = Historical_Event(**event.dict())
    engine.execute(db_event)
    return db_event

@app.get("/events/")
def list_events():
    """Récupérer tous les événements historiques"""
    events = engine.execute("SELECT * FROM historical_events").fetchall()
    return events

@app.get("/events/by_type/{event_type}")
def get_events_by_type(event_type: str):
    """Filtrer les événements par type"""
    events = engine.execute(
        "SELECT * FROM historical_events WHERE type = :type",
        {"type": event_type}
    ).fetchall()
    return events

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
