-- migrate:up
CREATE SCHEMA flynx;

-- Create the "events" table
CREATE TABLE flynx.events (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    image_path TEXT,
    description TEXT,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    location_name TEXT,
    location_coordinates POINT,
    location_url TEXT
);

CREATE INDEX index_id_value_events ON flynx.events (id, title, image_path);
CREATE INDEX index_start_date_events ON flynx.events (start_date, end_date);

-- migrate:down

-- Drop the "events" table
DROP TABLE IF EXISTS flynx.events;

-- Drop the "flynx" schema
DROP SCHEMA IF EXISTS flynx;