-- Seed data for Travel-Web (PostgreSQL)
-- Idempotent inserts using ON CONFLICT DO NOTHING
-- Assumes schema is already migrated / created.

BEGIN;

-- Destinations
INSERT INTO catalog_destination (name, slug, description, country, region, tags, is_active)
VALUES
  ('Ha Long Bay', 'ha-long-bay', 'Vịnh Hạ Long di sản thiên nhiên thế giới', 'Vietnam', 'Quang Ninh', 'beach,cruise,family', TRUE),
  ('Da Nang', 'da-nang', 'Thành phố biển năng động', 'Vietnam', 'Da Nang', 'beach,city,couple', TRUE)
ON CONFLICT (slug) DO NOTHING;

-- Tours
INSERT INTO tours_tour (tour_id, name, description, price, duration, location, is_active, created_at, updated_at)
VALUES
  (1001, 'Ha Long 3N2Đ', 'Tham quan vịnh, ngủ đêm trên tàu', 450.00, 3, 'Quang Ninh', TRUE, NOW(), NOW()),
  (1002, 'Bà Nà Hills 1N', 'Check-in Cầu Vàng, vườn hoa', 120.00, 1, 'Da Nang', TRUE, NOW(), NOW())
ON CONFLICT (tour_id) DO NOTHING;

-- Hotels
INSERT INTO hotels_hotel (hotel_id, name, description, price, location, amenities, rooms_available, is_active, created_at, updated_at)
VALUES
  (2001, 'Ha Long Seaview', 'Khách sạn view biển', 80.00, 'Quang Ninh', 'Wifi,Pool,Buffet', 20, TRUE, NOW(), NOW()),
  (2002, 'Danang Riverside', 'Gần sông Hàn, trung tâm', 75.00, 'Da Nang', 'Wifi,Gym,Breakfast', 25, TRUE, NOW(), NOW())
ON CONFLICT (hotel_id) DO NOTHING;

-- Flights
INSERT INTO flight_flight (flight_id, flight_number, departure, destination, departure_time, arrival_time, price, airline, seats_available, is_active, created_at, updated_at)
VALUES
  (3001, 'VN123', 'Ha Noi', 'Ha Long', NOW() + INTERVAL '3 day', NOW() + INTERVAL '3 day 2 hour', 90.00, 'Vietnam Airlines', 50, TRUE, NOW(), NOW()),
  (3002, 'VN456', 'Ho Chi Minh', 'Da Nang', NOW() + INTERVAL '5 day', NOW() + INTERVAL '5 day 1 hour', 110.00, 'Vietnam Airlines', 60, TRUE, NOW(), NOW())
ON CONFLICT (flight_id) DO NOTHING;

-- Packages
INSERT INTO catalog_package (id, title, destination_id, description, base_price, label, is_active, created_at, updated_at)
VALUES
  (4001, 'Combo Ha Long 3N2Đ', (SELECT id FROM catalog_destination WHERE slug='ha-long-bay'), 'Tour + khách sạn + flight nội địa', 650.00, 'family', TRUE, NOW(), NOW()),
  (4002, 'Combo Da Nang 2N1Đ', (SELECT id FROM catalog_destination WHERE slug='da-nang'), 'City tour + hotel trung tâm + flight', 320.00, 'couple', TRUE, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- Package relations
INSERT INTO catalog_package_tours (package_id, tour_id) VALUES
  (4001, 1001),
  (4002, 1002)
ON CONFLICT DO NOTHING;

INSERT INTO catalog_package_hotels (package_id, hotel_id) VALUES
  (4001, 2001),
  (4002, 2002)
ON CONFLICT DO NOTHING;

INSERT INTO catalog_package_flights (package_id, flight_id) VALUES
  (4001, 3001),
  (4002, 3002)
ON CONFLICT DO NOTHING;

COMMIT;

-- Fare rules seed
INSERT INTO catalog_airlinefarerule (carrier, route_type, trip_type, base_price, multiplier_advance, tax_fee, currency, is_active)
VALUES
  ('vietjet', 'domestic', 'oneway', 900000, 0.005, 150000, 'VND', TRUE),
  ('vietjet', 'domestic', 'roundtrip', 850000, 0.006, 250000, 'VND', TRUE),
  ('vna', 'international', 'oneway', 3500000, 0.008, 400000, 'VND', TRUE),
  ('vna', 'international', 'roundtrip', 3200000, 0.009, 700000, 'VND', TRUE)
ON CONFLICT DO NOTHING;

-- Visa requirement seed (sample)
INSERT INTO catalog_visarequirement (country_code, visa_required, note)
VALUES
  ('US', TRUE, 'Cần visa Hoa Kỳ'),
  ('JP', TRUE, 'Cần visa Nhật Bản'),
  ('SG', FALSE, 'Miễn visa dưới 30 ngày')
ON CONFLICT (country_code) DO NOTHING;

