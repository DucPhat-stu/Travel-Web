-- Schema updates for new features (PostgreSQL)
-- Include in migration/DDL runs before seeding data.

-- 1) catalog_destination
CREATE TABLE IF NOT EXISTS catalog_destination (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    country VARCHAR(120),
    region VARCHAR(120),
    best_season VARCHAR(120),
    tags VARCHAR(255),
    hero_image VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2) catalog_package
CREATE TABLE IF NOT EXISTS catalog_package (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    destination_id INTEGER NOT NULL REFERENCES catalog_destination(id) ON DELETE CASCADE,
    description TEXT,
    base_price NUMERIC(12,2) NOT NULL,
    label VARCHAR(50),
    rating_cached NUMERIC(3,2),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3) catalog_review (generic FK)
CREATE TABLE IF NOT EXISTS catalog_review (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_user(user_id) ON DELETE CASCADE,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    object_id INTEGER NOT NULL,
    rating SMALLINT NOT NULL DEFAULT 5,
    comment TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4) catalog_comment
CREATE TABLE IF NOT EXISTS catalog_comment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users_user(user_id) ON DELETE CASCADE,
    review_id INTEGER NOT NULL REFERENCES catalog_review(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 5) M2M tables for package relations (aligns with Django defaults)
CREATE TABLE IF NOT EXISTS catalog_package_tours (
    id SERIAL PRIMARY KEY,
    package_id INTEGER NOT NULL REFERENCES catalog_package(id) ON DELETE CASCADE,
    tour_id INTEGER NOT NULL REFERENCES tours_tour(tour_id) ON DELETE CASCADE,
    UNIQUE (package_id, tour_id)
);

CREATE TABLE IF NOT EXISTS catalog_package_hotels (
    id SERIAL PRIMARY KEY,
    package_id INTEGER NOT NULL REFERENCES catalog_package(id) ON DELETE CASCADE,
    hotel_id INTEGER NOT NULL REFERENCES hotels_hotel(hotel_id) ON DELETE CASCADE,
    UNIQUE (package_id, hotel_id)
);

CREATE TABLE IF NOT EXISTS catalog_package_flights (
    id SERIAL PRIMARY KEY,
    package_id INTEGER NOT NULL REFERENCES catalog_package(id) ON DELETE CASCADE,
    flight_id INTEGER NOT NULL REFERENCES flight_flight(flight_id) ON DELETE CASCADE,
    UNIQUE (package_id, flight_id)
);

-- 6) users_user_token
CREATE TABLE IF NOT EXISTS users_user_token (
    id SERIAL PRIMARY KEY,
    key VARCHAR(40) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users_user(user_id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 7) bookings_booking: add package_id FK (if not present)
ALTER TABLE bookings_booking
    ADD COLUMN IF NOT EXISTS package_id INTEGER NULL REFERENCES catalog_package(id) ON DELETE SET NULL;

-- 8) hotels_hotel: add rooms_available
ALTER TABLE hotels_hotel
    ADD COLUMN IF NOT EXISTS rooms_available INTEGER NOT NULL DEFAULT 0;

-- 9) flight_flight: add seats_available
ALTER TABLE flight_flight
    ADD COLUMN IF NOT EXISTS seats_available INTEGER NOT NULL DEFAULT 0;

-- Index hints for filters
CREATE INDEX IF NOT EXISTS idx_catalog_package_label ON catalog_package(label);
CREATE INDEX IF NOT EXISTS idx_catalog_package_price ON catalog_package(base_price);
CREATE INDEX IF NOT EXISTS idx_catalog_destination_active ON catalog_destination(is_active);
CREATE INDEX IF NOT EXISTS idx_hotels_rooms_available ON hotels_hotel(rooms_available);
CREATE INDEX IF NOT EXISTS idx_flights_seats_available ON flight_flight(seats_available);

-- 10) Airline fare rules
CREATE TABLE IF NOT EXISTS catalog_airlinefarerule (
    id SERIAL PRIMARY KEY,
    carrier VARCHAR(20) NOT NULL,
    route_type VARCHAR(20) NOT NULL,
    trip_type VARCHAR(20) NOT NULL,
    base_price NUMERIC(12,2) NOT NULL,
    multiplier_advance NUMERIC(6,4) NOT NULL DEFAULT 0.0100,
    tax_fee NUMERIC(10,2) NOT NULL DEFAULT 0,
    currency VARCHAR(10) NOT NULL DEFAULT 'VND',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (carrier, route_type, trip_type)
);

-- 11) Visa requirement
CREATE TABLE IF NOT EXISTS catalog_visarequirement (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(5) UNIQUE NOT NULL,
    visa_required BOOLEAN NOT NULL DEFAULT TRUE,
    note TEXT
);

