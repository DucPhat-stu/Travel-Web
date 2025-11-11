# Model Design

## 1. User
- Bảng: users_user
- Mô tả: Lưu thông tin người dùng và phân quyền.
- Trường:
  + user_id (PK, auto)
  + full_name (varchar)
  + email (varchar, unique)
  + phone (varchar)
  + password (hash)
  + address (varchar)
  + role (varchar: user/admin)

## 2. Tour
- Bảng: tours_tour
- Mô tả: Danh sách tour du lịch.
- Trường:
  + tour_id (PK, auto)
  + name (varchar)
  + location (varchar)
  + price (decimal)
  + duration (varchar)
  + description (text)
  + image (file/url)

## 3. Hotel
- Bảng: hotels_hotel
- Mô tả: Danh sách khách sạn.
- Trường:
  + hotel_id (PK, auto)
  + name (varchar)
  + location (varchar)
  + price_per_night (decimal)
  + rating (float)
  + description (text)
  + image (file/url)

## 4. Flight
- Bảng: flight_flight
- Mô tả: Danh sách chuyến bay.
- Trường:
  + flight_id (PK, auto)
  + airline (varchar)
  + origin (varchar)
  + destination (varchar)
  + departure_time (datetime)
  + price (decimal)

## 5. Booking
- Bảng: bookings_booking
- Mô tả: Lưu đơn đặt dịch vụ.
- Trường:
  + booking_id (PK, auto)
  + user_id (FK -> User)
  + tour_id (FK -> Tour, null)
  + hotel_id (FK -> Hotel, null)
  + flight_id (FK -> Flight, null)
  + quantity_people (int)
  + booking_date (datetime)
  + status (varchar: pending/confirmed/cancelled)

## 6. ChatLog
- Bảng: chatbot_chatlog
- Mô tả: Lịch sử chat giữa user và chatbot.
- Trường:
  + chat_id (PK, auto)
  + user_id (FK -> User)
  + message_user (text)
  + message_bot (text)
  + timestamp (datetime)
