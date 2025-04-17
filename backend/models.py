# backend/models.py

class HistoricalEvent:
    """Modèle représentant un événement historique (sans SQLAlchemy)"""

    def __init__(self, id, name, type, latitude, longitude, description, era, protagonistes, continent, date_text, image_url=None, video_url=None, source_url=None):
        self.id = id
        self.name = name
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.description = description
        self.era = era
        self.protagonistes = protagonistes
        self.continent = continent
        self.date_text = date_text
        self.image_url = image_url if image_url else None
        self.video_url = video_url if video_url else None
        self.source_url = source_url if source_url else None

    def to_dict(self):
        """Convertir l'objet en dictionnaire"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
            "era": self.era,
            "protagonistes": self.protagonistes,
            "continent": self.continent,
            "date_text": self.date_text,
            "image_url": self.image_url or None,
            "video_url": self.video_url or None,
            "source_url": self.source_url or None,
        }