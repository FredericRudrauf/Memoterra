#backend/main.py
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from database import get_db
from schemas import EventCreate, Event
import uvicorn
import logging
from typing import List
import asyncio

# Fix pour Windows et les connexions async avec psycopg
if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Carte Historique Interactive")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/events/", response_model=Event)
async def create_event(event: EventCreate, db=Depends(get_db)):
    """Créer un nouvel événement historique"""
    try:
        query = """
                INSERT INTO historical_events (name, id_type, latitude, longitude, description, id_era, protagonistes, id_continent, date_text)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name, id_type, latitude, longitude, description, id_era, protagonistes, id_continent, date_text
                """
        await db.execute(query, (event.name, event.id_type, event.latitude, event.longitude,
                                 event.description, event.id_era, event.protagonistes, event.id_continent,
                                 event.date_text))
        row = await db.fetchone()

        if row:
            columns = [desc[0] for desc in db.description]
            return dict(zip(columns, row))
        else:
            raise HTTPException(status_code=500, detail="Erreur lors de l'insertion de l'événement")

    except Exception as e:
        logging.exception("Erreur lors de la création de l'événement")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events/", response_model=List[Event])
async def list_events(db=Depends(get_db)):
    """Récupérer tous les événements historiques avec l'image associée"""
    try:
        query = """
            SELECT 
                he.id,
                he.name,
                te.name_type AS type,
                he.latitude,
                he.longitude,
                he.description,
                e.name_era AS era,
                he.protagonistes, 
                c.name_continent AS continent,
                he.date_text,
                MAX(CASE WHEN lw.type_lien = 'photo' THEN lw.adresse ELSE NULL END) AS image_url,
                MAX(CASE WHEN lw.type_lien = 'video' THEN lw.adresse ELSE NULL END) AS video_url,
                MAX(CASE WHEN lw.type_lien = 'source' THEN lw.adresse ELSE NULL END) AS source_url
            FROM historical_events he
            JOIN type_events te ON he.id_type = te.id
            JOIN eras e ON he.id_era = e.id
            JOIN continents c ON he.id_continent = c.id
            LEFT JOIN liens_web lw ON he.id = lw.id_event
            GROUP BY he.id, te.name_type, e.name_era, c.name_continent
            ORDER BY he.id;
        """
        async with db as conn:
            await conn.execute(query)
            rows = await conn.fetchall()
            columns = [desc[0] for desc in conn.description]

        events = []
        for row in rows:
            event_dict = dict(zip(columns, row))
            events.append(event_dict)

        return events

    except Exception as e:
        logging.exception("Erreur lors de la récupération des événements")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/by_types", response_model=List[Event])
async def get_events_by_types(types: List[str] = Query(None), db=Depends(get_db)):
    """Filtrer les événements par plusieurs types"""
    try:
        if not types:
            raise HTTPException(status_code=400, detail="Veuillez fournir au moins un type d'événement.")

        placeholders = ', '.join(['%s'] * len(types))  # Génère le bon nombre de placeholders (%s, %s, ...)
        query = f"""SELECT he.id, he.name, te.name_type AS type, he.latitude, he.longitude, he.description, 
                           e.name_era AS era, he.protagonistes, c.name_continent AS continent, he.date_text 
                    FROM historical_events he
                    JOIN type_events te ON he.id_type = te.id
                    JOIN eras e ON he.id_era = e.id
                    JOIN continents c ON he.id_continent = c.id
                    WHERE te.name_type IN ({placeholders})"""

        async with db as conn:
            await conn.execute(query, tuple(types))  # Passer la liste de types comme arguments
            rows = await conn.fetchall()
            columns = [desc[0] for desc in conn.description]

        if not rows:
            return []  # Retourner une liste vide si aucun événement trouvé

        events = [dict(zip(columns, row)) for row in rows]
        return events

    except Exception as e:
        logging.exception("Erreur lors du filtrage des événements par types")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events/filtered", response_model=List[Event])
async def get_filtered_events(
    types: List[str] = Query(None),
    continents: List[str] = Query(None),
    eras: List[str] = Query(None),
    db=Depends(get_db)
):
    """Filtrer les événements par types, continents et ères"""
    try:
        where_clauses = []
        params = []

        if types:
            placeholders_types = ', '.join(['%s'] * len(types))
            where_clauses.append(f"te.name_type IN ({placeholders_types})")
            params.extend(types)

        if continents:
            placeholders_continents = ', '.join(['%s'] * len(continents))
            where_clauses.append(f"c.name_continent IN ({placeholders_continents})")
            params.extend(continents)

        if eras:
            placeholders_eras = ', '.join(['%s'] * len(eras))
            where_clauses.append(f"e.name_era IN ({placeholders_eras})")
            params.extend(eras)

        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"

        query = f"""
            SELECT 
                he.id,
                he.name,
                te.name_type AS type,
                he.latitude,
                he.longitude,
                he.description,
                e.name_era AS era,
                he.protagonistes, 
                c.name_continent AS continent,
                he.date_text,
                MAX(CASE WHEN lw.type_lien = 'photo' THEN lw.adresse ELSE NULL END) AS image_url,
                MAX(CASE WHEN lw.type_lien = 'video' THEN lw.adresse ELSE NULL END) AS video_url,
                MAX(CASE WHEN lw.type_lien = 'source' THEN lw.adresse ELSE NULL END) AS source_url
            FROM historical_events he
            JOIN type_events te ON he.id_type = te.id
            JOIN eras e ON he.id_era = e.id
            JOIN continents c ON he.id_continent = c.id
            LEFT JOIN liens_web lw ON he.id = lw.id_event
            WHERE {where_clause}
            GROUP BY he.id, te.name_type, e.name_era, c.name_continent
            ORDER BY he.id;
        """

        async with db as conn:
            await conn.execute(query, tuple(params))
            rows = await conn.fetchall()
            columns = [desc[0] for desc in conn.description]

        return [dict(zip(columns, row)) for row in rows] if rows else []

    except Exception as e:
        logging.exception("Erreur lors du filtrage des événements")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
