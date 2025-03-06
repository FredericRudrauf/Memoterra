# backend/database.py
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Récupérer les informations de connexion
DB_USER = os.getenv("DB_USER", "mapuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password_with_*")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "historical_map")

# Encoder explicitement le mot de passe pour gérer les caractères spéciaux
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# Construction de l'URL avec le mot de passe encodé
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"

print(f"Connexion à: postgresql://{DB_USER}:***@{DB_HOST}/{DB_NAME}")  # Ne pas afficher le vrai mot de passe

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
