# API Endpoints

## Auth
- POST /users/register      : Tạo tài khoản mới
- POST /users/login         : Đăng nhập
- POST /users/logout        : Đăng xuất
- POST /users/forget        : Yêu cầu khôi phục mật khẩu
- POST /users/reset         : Đặt lại mật khẩu

## Tours
- GET    /tours/list        : Lấy danh sách tour
- GET    /tours/detail/<id> : Lấy thông tin tour
- POST   /tours/create      : Thêm tour (admin)
- POST   /tours/update/<id> : Cập nhật tour (admin)
- POST   /tours/delete/<id> : Xóa tour (admin)

## Hotels
- GET    /hotels/list
- GET    /hotels/detail/<id>
- POST   /hotels/create       (admin)
- POST   /hotels/update/<id>  (admin)
- POST   /hotels/delete/<id>  (admin)

## Flight
- GET    /flight/list
- GET    /flight/detail/<id>
- POST   /flight/create       (admin)
- POST   /flight/update/<id>  (admin)
- POST   /flight/delete/<id>  (admin)

## Booking
- POST   /booking/create        : Tạo đơn đặt dịch vụ
- GET    /booking/list          : Xem danh sách booking (user)
- POST   /booking/cancel/<id>   : Hủy booking (user)
- GET    /booking/manage        : Xem danh sách booking (admin)
- POST   /booking/confirm/<id>  : Xác nhận booking (admin)

## Chatbot
- POST   /chatbot/message       : Gửi tin nhắn và nhận phản hồi
- GET    /chatbot/logs          : Xem lịch sử hội thoại (admin)
