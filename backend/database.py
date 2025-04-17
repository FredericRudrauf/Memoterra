# backend/database.py
import os
import urllib.parse
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv
from fastapi import HTTPException
import logging

load_dotenv()

DB_USER = os.getenv("DB_USER", "devFred")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Victoria421")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "historical_map")

encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"

pool = None  # Déclarer le pool globalement mais sans l'instancier immédiatement

async def init_db():
    """Initialiser le pool de connexions asynchrones."""
    global pool
    if pool is None:
        try:
            pool = AsyncConnectionPool(DATABASE_URL, min_size=1, max_size=5)
            await pool.open()  # Ouvrir le pool explicitement
        except Exception as e:
            logging.error(f"Erreur lors de l'initialisation du pool : {e}")
            raise HTTPException(status_code=500, detail="Erreur de base de données")

async def get_db():
    """Obtenir une connexion depuis le pool."""
    if pool is None:
        await init_db()  # S'assurer que le pool est bien initialisé
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            yield cur
