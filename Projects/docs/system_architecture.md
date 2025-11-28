# I. MÔ TẢ KIẾN TRÚC HỆ THỐNG
Hệ thống đặt tour du lịch được xây dựng theo mô hình kiến trúc nhiều tầng (multi-layer architecture), giúp phân tách rõ ràng giữa các chức năng, dễ bảo trì và mở rộng. Kiến trúc gồm các tầng sau:

## 1. Tầng giao diện người dùng (Presentation Layer)
Đây là tầng đầu tiên mà người dùng tương tác trực tiếp. Giao diện được thiết kế thân thiện, dễ sử dụng, hỗ trợ cả người dùng phổ thông và quản trị viên.
- Web UI: Giao diện web cho người dùng để tìm kiếm, đặt tour, khách sạn, chuyến bay.
- Chatbot UI: Giao diện trò chuyện với chatbot, hỗ trợ người dùng đặt dịch vụ hoặc hỏi đáp nhanh.
## 2. Tầng ứng dụng (Application Layer)
Tầng này xử lý các yêu cầu từ giao diện người dùng và điều phối các chức năng nghiệp vụ. Được xây dựng bằng framework Django, tầng này bao gồm các module chính:
- User Service: Quản lý đăng ký, đăng nhập, thông tin người dùng, phân quyền.
- Service Booking Service: Xử lý logic đặt tour, khách sạn, chuyến bay, quản lý trạng thái đơn đặt.
- Chatbot Service: Tích hợp chatbot để phản hồi người dùng, gợi ý dịch vụ, hỗ trợ đặt nhanh.
- Admin Service: Cung cấp chức năng quản lý cho quản trị viên như thêm/sửa/xóa dịch vụ và xem thống kê.
## 3. Tầng nghiệp vụ (Business Logic Layer)
Tầng này chứa các quy tắc nghiệp vụ cốt lõi của hệ thống:
- Booking Logic: Kiểm tra điều kiện đặt dịch vụ, xử lý trạng thái đơn hàng, gửi thông báo xác nhận.
 Tour/Hotel/Flight Management: Kiểm tra tính hợp lệ khi thêm/sửa/xóa dịch vụ.
- Chatbot NLP: Phân tích ngôn ngữ tự nhiên để hiểu yêu cầu người dùng và phản hồi phù hợp.
## 4. Tầng truy cập dữ liệu (Data Access Layer)
Tầng này đóng vai trò trung gian giữa tầng nghiệp vụ và cơ sở dữ liệu:
- ORM (Object-Relational Mapping): Sử dụng Django ORM để truy vấn dữ liệu một cách an toàn và hiệu quả.
- External API Calls: Giao tiếp với các dịch vụ bên ngoài (ví dụ: API chuyến bay, thanh toán).
## 5. Tầng cơ sở dữ liệu (Data Layer)
Tầng cuối cùng lưu trữ toàn bộ dữ liệu của hệ thống:
- Hệ quản trị cơ sở dữ liệu: PostgreSQL hoặc MySQL.
- Các bảng dữ liệu chính:
-- User: Thông tin người dùng.
-- Booking: Đơn đặt dịch vụ.
-- Tour, Hotel, Flight: Dữ liệu dịch vụ.
-- ChatLog: Lịch sử trò chuyện với chatbot.
- Bảo mật và triển khai
- Xác thực & phân quyền: Sử dụng JWT hoặc session-based authentication để bảo vệ API và phân quyền truy cập.
- Triển khai: Sử dụng Docker và docker-compose để đóng gói ứng dụng và triển khai trên cloud như AWS, Heroku hoặc Azure.
Sao lưu & phục hồi: Cấu hình backup định kỳ cho cơ sở dữ liệu, đảm bảo an toàn dữ liệu.

# II. MÔ TẢ CÁC MODULE
Hệ thống được tổ chức theo kiến trúc module hóa, mỗi module đảm nhiệm một chức năng riêng biệt, giúp dễ dàng mở rộng, bảo trì và kiểm thử.

## 1. Module users
- Quản lý thông tin người dùng (họ tên, email, số điện thoại, địa chỉ…)
- Đăng ký và đăng nhập người dùng
- Xác thực và phân quyền (user/admin)
- Mã hóa mật khẩu và bảo vệ thông tin cá nhân
## 2. Module bookings
- Tạo, cập nhật, hủy đơn đặt tour, khách sạn, chuyến bay
- Quản lý trạng thái đơn đặt (pending, confirmed, canceled)
- Tính toán số lượng người, tổng chi phí
- Liên kết với các dịch vụ: tour, khách sạn, chuyến bay
## 3. Module chatbot
- Trò chuyện với người dùng qua giao diện tin nhắn
- Gợi ý tour, khách sạn, chuyến bay phù hợp
- Trả lời câu hỏi thường gặp
- Hỗ trợ đặt dịch vụ qua hội thoại
## 4. Module admin-panel
- Giao diện quản trị cho admin
- Quản lý người dùng, tour, khách sạn, chuyến bay
- Xem thống kê hệ thống: số lượng đặt, doanh thu, lượt truy cập
- Phân quyền và kiểm tra hoạt động
## 5. Module tours
- Quản lý thông tin tour du lịch: tên tour, địa điểm, giá, thời lượng, mô tả
- Liên kết với đơn đặt dịch vụ
- Hiển thị danh sách tour cho người dùng
## 6. Module hotels
- Quản lý thông tin khách sạn: tên, địa điểm, giá phòng, đánh giá, mô tả
- Hiển thị danh sách khách sạn cho người dùng
- Liên kết với đơn đặt dịch vụ
## 7. Module flights
- Quản lý thông tin chuyến bay: hãng bay, điểm đi, điểm đến, thời gian khởi hành, giá vé
- Hiển thị danh sách chuyến bay cho người dùng
- Liên kết với đơn đặt dịch vụ
## 8. Module core
- Cấu hình chung cho toàn hệ thống
- Xử lý lỗi, thông báo, middleware
- Tích hợp các dịch vụ bên ngoài (email, API…)

## 9. Module data
- Chứa dữ liệu mẫu để seed vào hệ thống
- Hỗ trợ kiểm thử và demo hệ thống