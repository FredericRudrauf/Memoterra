-- database/init.sql
CREATE TABLE historical_events (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    date DATE,
    description TEXT,
    era VARCHAR(100)
);

-- Insertions d'exemple
INSERT INTO historical_events
(name, type, latitude, longitude, date, description, era)
VALUES
('Bataille de Waterloo', 'bataille', 50.4620, 4.4000, '1815-06-18',
 'Bataille décisive qui a mis fin à l''empire napoléonien', 'Époque napoléonienne'),
('Chute du Mur de Berlin', 'événement politique', 52.5163, 13.3777, '1989-11-09',
 'Chute symbolique du mur séparant Berlin-Est et Berlin-Ouest', 'Guerre Froide');
