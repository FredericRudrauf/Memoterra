// frontend/src/components/HistoricalMap.js
import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { MapContainer, TileLayer, Marker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import '../styles/map.css';
import '../styles/vintage.css';
import '../styles/navbar.css';
import '../styles/sidebar.css';
import '../styles/AboutPage.css';

const icons = {
    'bataille': L.icon({ iconUrl: '/assets/sword-icon.png', iconSize: [30, 30] }),
    'site': L.icon({ iconUrl: '/assets/castle-icon.png', iconSize: [30, 30] }),
    default: L.icon({ iconUrl: '/assets/default-icon.png', iconSize: [25, 25] })
};

const initialTypeFilters = ["bataille", "site"];
const initialContinentFilters = ["Europe", "Asie", "Afrique", "Amérique du Nord", "Amérique du Sud", "Océanie"];
const initialEraFilters = ["Antiquité", "Moyen Âge", "Période moderne", "Époque contemporaine"];

const Navbar = () => (
    <nav className="navbar">
        <div className="navbar-title">
            <img src="../assets/logo.png" alt="Logo" className="navbar-logo" />
            <h1>MEMOTERRA</h1>
        </div>
        <ul className="navbar-menu">
            <li><Link to="/">Accueil</Link></li>
            <li><Link to="/about">À propos</Link></li>
        </ul>
    </nav>
);

const Sidebar = ({ filters, setFilters, continentFilters, setContinentFilters, eraFilters, setEraFilters }) => {

    const handleCheckboxChange = (event) => {
        const { value, checked } = event.target;
        setFilters((prevFilters) =>
            checked ? [...prevFilters, value] : prevFilters.filter(f => f !== value)
        );
    };

    const handleFilterChange = (event, setFilter) => {
        const { value, checked } = event.target;
        setFilter((prevFilters) =>
            checked ? [...prevFilters, value] : prevFilters.filter(f => f !== value)
        );
    };

    return (
        <div className="sidebar"> {/* Ajout d'un div parent */}
            <h3>Types</h3>
            <div className="filter-options">
                <label>
                    <input
                        type="checkbox"
                        value="bataille"
                        checked={filters.includes("bataille")}
                        onChange={handleCheckboxChange}
                    />
                    Batailles
                </label>
                <label>
                    <input
                        type="checkbox"
                        value="site"
                        checked={filters.includes("site")}
                        onChange={handleCheckboxChange}
                    />
                    Sites
                </label>
            </div>
            <div className="filter-options">
                <h3>Continents</h3>
                <label><input type="checkbox" value="Europe" checked={continentFilters.includes("Europe")} onChange={(e) => handleFilterChange(e, setContinentFilters)} />Europe</label>
                <label><input type="checkbox" value="Asie" checked={continentFilters.includes("Asie")} onChange={(e) => handleFilterChange(e, setContinentFilters)} />Asie</label>
                <label><input type="checkbox" value="Afrique" checked={continentFilters.includes("Afrique")} onChange={(e) => handleFilterChange(e, setContinentFilters)} />Afrique</label>
                <label><input type="checkbox" value="Amérique du Nord" checked={continentFilters.includes("Amérique du Nord")} onChange={(e) => handleFilterChange(e, setContinentFilters)} />Amérique du Nord</label>
                <label><input type="checkbox" value="Amérique du Sud" checked={continentFilters.includes("Amérique du Sud")} onChange={(e) => handleFilterChange(e, setContinentFilters)} />Amérique du Sud</label>
                <label><input type="checkbox" value="Océanie" checked={continentFilters.includes("Océanie")} onChange={(e) => handleFilterChange(e, setContinentFilters)} />Océanie</label>
            </div>
            <div className="filter-options">
                <h3>Périodes</h3>
                <label><input type="checkbox" value="Antiquité" checked={eraFilters.includes("Antiquité")} onChange={(e) => handleFilterChange(e, setEraFilters)} />Antiquité</label>
                <label><input type="checkbox" value="Moyen Âge" checked={eraFilters.includes("Moyen Âge")} onChange={(e) => handleFilterChange(e, setEraFilters)} />Moyen Âge</label>
                <label><input type="checkbox" value="Période moderne" checked={eraFilters.includes("Période moderne")} onChange={(e) => handleFilterChange(e, setEraFilters)} />Période moderne</label>
                <label><input type="checkbox" value="Époque contemporaine" checked={eraFilters.includes("Époque contemporaine")} onChange={(e) => handleFilterChange(e, setEraFilters)} />Époque contemporaine</label>
            </div>
        </div>
    );
};

const HistoricalMap = () => {
    const [events, setEvents] = useState([]);
    const [filters, setFilters] = useState(initialTypeFilters);
    const [continentFilters, setContinentFilters] = useState(initialContinentFilters);
    const [eraFilters, setEraFilters] = useState(initialEraFilters);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const infoPanelRef = useRef(null);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                let url = 'http://localhost:8000/events/filtered?';
                const queryParams = [];

                if (filters.length > 0) {
                    filters.forEach(type => queryParams.push(`types=${encodeURIComponent(type)}`));
                } else {
                    setEvents([]);
                    return;
                }

                if (continentFilters.length > 0) {
                    continentFilters.forEach(continent => queryParams.push(`continents=${encodeURIComponent(continent)}`));
                } else {
                    setEvents([]);
                    return;
                }

                if (eraFilters.length > 0) {
                    eraFilters.forEach(era => queryParams.push(`eras=${encodeURIComponent(era)}`));
                } else {
                    setEvents([]);
                    return;
                }

                url += queryParams.join('&');
                const response = await axios.get(url);
                setEvents(response.data);
            } catch (error) {
                console.error("Erreur lors du chargement des événements", error);
            }
        };
        fetchEvents();
    }, [filters, continentFilters, eraFilters]);

    const handleMapClick = (e) => {
        if (
            selectedEvent &&
            infoPanelRef.current &&
            !infoPanelRef.current.contains(e.target)
        ) {
            setSelectedEvent(null);
        }
    };

    return (
        <div className="map-wrapper" onClick={handleMapClick}>
            <Sidebar
                filters={filters}
                setFilters={setFilters}
                continentFilters={continentFilters}
                setContinentFilters={setContinentFilters}
                eraFilters={eraFilters}
                setEraFilters={setEraFilters}
            />
            <div className="map-container">
                <MapContainer center={[30, 0]} zoom={3} style={{ height: '92vh', width: '100%' }}>
                    <TileLayer
                        url="http://services.arcgisonline.com/arcgis/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}"
                        attribution="Map tiles by National Geographic"
                    />
                    {events.map((event) => (
                        <Marker
                            key={event.id}
                            position={[event.latitude, event.longitude]}
                            icon={icons[event.type] || icons.default}
                            eventHandlers={{
                                click: (e) => {
                                    e.originalEvent.stopPropagation();
                                    setSelectedEvent(event);
                                }
                            }}
                        />
                    ))}
                </MapContainer>
            </div>

            {selectedEvent && (
                <div ref={infoPanelRef} className="info-panel right-0">
                    <button className="close-button" onClick={() => setSelectedEvent(null)}>×</button>

                    <div className="info-content">

                        <h3>{selectedEvent.name}</h3>

                        <p><strong>Période :</strong> {selectedEvent.era}</p>
                        <p><strong>Date :</strong> {selectedEvent.date_text}</p>

                        {selectedEvent.image_url && selectedEvent.image_url.trim() !== "" && (
                            <img
                                src={selectedEvent.image_url}
                                alt={selectedEvent.name}
                                className="event-image"
                                onError={() => console.error("Erreur de chargement de l'image :", selectedEvent.image_url)}
                                onLoad={() => console.log("Image chargée :", selectedEvent.image_url)}
                            />
                        )}

                        <p><strong>Protagonistes :</strong> {selectedEvent.protagonistes}</p>

                        <div className="event-description">
                            <p><strong>Description :</strong> {selectedEvent.description}</p>
                        </div>

                        {selectedEvent.video_url && selectedEvent.video_url.trim() !== "" && (
                            <a href={selectedEvent.video_url} target="_blank" rel="noopener noreferrer" className="video-link">
                                🎥 Regarder une vidéo
                            </a>
                        )}

                        {selectedEvent.source_url && selectedEvent.source_url.trim() !== "" && (
                            <p>
                                <strong>Source :</strong><br />
                                <a href={selectedEvent.source_url} target="_blank" rel="noopener noreferrer" className="source-link">
                                    🔗 {selectedEvent.source_url}
                                </a>
                            </p>
                        )}

                    </div>
                </div>
            )}
        </div>
    );
};

const AboutPage = () => (
    <div className="about-container">
        <div className="about-content">
            <div className="about-memoterra">
                <h2>À propos de Memoterra</h2>
                <p>Memoterra est une application de cartographie historique qui permet d'explorer des événements passés sur une carte interactive.</p>
                <video width="80%" controls autoPlay loop muted>
                    <source src="/assets/memoterra-presentation.mp4" type="video/mp4" />
                    Votre navigateur ne supporte pas la lecture des vidéos.
                </video>
            </div>
            <div className="about-author">
                <h2>À propos de l'auteur</h2>
                <div className="author-info">
                    <img src="/assets/author-photo.png" alt="Frédéric Rudrauf" />
                    <div>
                        <p>Développé par Frédéric Rudrauf, passionné d'histoire et de technologie.</p>
                        <p>J'ai créé Memoterra pour rendre l'histoire plus accessible et interactive.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
);

const App = () => (
    <Router>
        <Navbar />
        <Routes>
            <Route path="/" element={<HistoricalMap />} />
            <Route path="/about" element={<AboutPage />} />
        </Routes>
    </Router>
);

export default App;