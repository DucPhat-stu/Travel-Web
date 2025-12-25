from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from datetime import datetime
import random
import string

from .models import Booking, Ticket, Package
from .services import BookingService


def booking_list(request):
    if request.method == 'POST':
        # Xử lý form từ trang chủ
        destination = request.POST.get('destination', '')
        checkin = request.POST.get('checkin', '')
        checkout = request.POST.get('checkout', '')
        adults = request.POST.get('adults', '1')
        children = request.POST.get('children', '0')
        tour_type = request.POST.get('tour_type', '')

        # Chuyển hướng đến trang tours với tham số tìm kiếm
        from django.urls import reverse
        url = reverse('tours:tour_list')
        params = []
        if destination:
            params.append(f'destination={destination}')
        if checkin:
            params.append(f'checkin={checkin}')
        if checkout:
            params.append(f'checkout={checkout}')
        if adults:
            params.append(f'adults={adults}')
        if children:
            params.append(f'children={children}')
        if tour_type:
            params.append(f'tour_type={tour_type}')

        if params:
            url += '?' + '&'.join(params)

        return redirect(url)

    # GET request - hiển thị danh sách booking của user
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    else:
        bookings = []

    context = {
        'bookings': bookings,
    }

    return render(request, 'booking.html', context)


def contact_booking(request, package_id):
    try:
        package = Package.objects.get(id=package_id, is_active=True)
    except Package.DoesNotExist:
        messages.error(request, 'Package không tồn tại hoặc không khả dụng')
        return redirect('tours:tour_list')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email:
            messages.error(request, 'Vui lòng nhập đầy đủ tên và email')
            return redirect('bookings:contact_booking', package_id=package_id)

        # Ở đây có thể gửi email hoặc lưu vào database
        # Hiện tại chỉ hiển thị thông báo thành công
        messages.success(request, f'Cảm ơn {name}! Chúng tôi sẽ liên hệ với bạn qua email {email} trong thời gian sớm nhất.')
        return redirect('tours:tour_list')

    context = {
        'package': package,
    }

    return render(request, 'contact.html', context)


def booking_details(request):
    # Mock data for now - in real implementation, get from session or POST
    booking_data = {
        'full_name': 'Nguyen Van A',
        'number_of_people': 2,
    }
    package = Package.objects.filter(is_active=True).first()  # Get first active package
    total_cost = 1000000
    flight_details = []
    hotel_details = []
    payment_methods = ['momo', 'zalopay', 'banking']

    context = {
        'booking_data': booking_data,
        'package': package,
        'total_cost': total_cost,
        'flight_details': flight_details,
        'hotel_details': hotel_details,
        'payment_methods': payment_methods,
    }

    return render(request, 'booking_details.html', context)


def confirm_payment(request):
    return redirect('bookings:booking_list')


def booking_confirm(request):
    messages.info(request, 'Chức năng cũ')
    return redirect('bookings:booking_list')


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    context = {
        'booking': booking,
    }
    return render(request, 'booking_detail.html', context)


@login_required(login_url='users:login')
def booking_history(request):
    if request.user.is_authenticated:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    else:
        bookings = []
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking_history.html', context)


@login_required(login_url='users:login')
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking đã được hủy')
    else:
        messages.error(request, 'Không thể hủy booking này')
    return redirect('bookings:booking_history')


def booking_api_recommendations(request):
    data = {'recommendations': []}
    from django.http import JsonResponse
    return JsonResponse(data)


def ticket_detail(request, ticket_id):
    if ticket_id == 'preview':
        preview_data = request.session.get('ticket_preview')
        if not preview_data:
            messages.error(request, 'Không tìm thấy thông tin vé xem trước')
            return redirect('bookings:booking_list')

        # Cập nhật passenger_name nếu chưa có hoặc user vừa đăng nhập
        from users.services import SessionService
        current_user = SessionService.get_current_user(request)
        if current_user and (not preview_data.get('passenger_name') or preview_data.get('passenger_name') == ''):
            preview_data['passenger_name'] = current_user.full_name or current_user.email
            request.session['ticket_preview'] = preview_data
            request.session.modified = True

        # Tạo object giả cho template
        class PreviewTicket:
            def __init__(self, data):
                self.ticket_id = 'preview'
                self.passenger_name = data['passenger_name']
                self.created_at = datetime.now()
                self.payment_method = ''
                self.total_cost = data['total_cost']
                self.tour_name = data.get('tour_name', 'Tour')
                self.destination_name = data.get('destination_name', '')
                self.flight_details = f"Tour: {data['tour_name']}\nĐiểm đến: {data['destination_name']}"
                self.hotel_room_details = "Tour không bao gồm khách sạn"
                # Mock booking object (reflect session booking_status if set)
                class MockBooking:
                    def __init__(self, status='pending'):
                        self.status = status
                    def get_status_display(self):
                        return 'Đã thanh toán' if self.status == 'paid' else 'Chưa thanh toán'

                self.booking = MockBooking(data.get('booking_status', 'pending'))
                self.payment_method = data.get('payment_method', '')

        ticket = PreviewTicket(preview_data)
        is_preview = True
        # If preview has been marked paid by the payment flow, reflect that
        booking_status = preview_data.get('booking_status', 'pending')
        can_pay = booking_status != 'paid'
    else:
        # Vé thật - yêu cầu đăng nhập
        if not request.user.is_authenticated:
            from django.urls import reverse
            from urllib.parse import quote
            login_url = reverse('users:login')
            next_url = quote(request.get_full_path(), safe='/')
            return redirect(f'{login_url}?next={next_url}')

        # Vé thật
        ticket = get_object_or_404(Ticket, ticket_id=ticket_id, booking__user=request.user)
        is_preview = False
        can_pay = ticket.booking.status != 'paid'

    context = {
        'ticket': ticket,
        'is_preview': is_preview,
        'can_pay': can_pay
    }

    return render(request, 'ticket.html', context)


@require_http_methods(["GET", "POST"])
def payment(request, ticket_id):
    # For preview ticket, don't require login yet (will check session)
    # For real tickets, require login
    if ticket_id != 'preview' and not request.user.is_authenticated:
        from django.urls import reverse
        from urllib.parse import quote
        login_url = reverse('users:login')
        next_url = quote(request.get_full_path(), safe='/')
        return redirect(f'{login_url}?next={next_url}')
    
    if ticket_id == 'preview':
        # Thanh toán cho vé xem trước
        preview_data = request.session.get('ticket_preview')
        if not preview_data:
            messages.error(request, 'Không tìm thấy thông tin vé xem trước. Vui lòng chọn tour trước.')
            return redirect('tours:tour_list')

        if request.method == 'POST':
            # Yêu cầu đăng nhập để thanh toán
            if not request.user.is_authenticated:
                messages.info(request, 'Vui lòng đăng nhập để hoàn tất thanh toán')
                from django.urls import reverse
                from urllib.parse import quote
                login_url = reverse('users:login')
                next_url = quote(request.get_full_path(), safe='/')
                return redirect(f'{login_url}?next={next_url}')
            
            payment_method = request.POST.get('payment_method')
            if not payment_method:
                messages.error(request, 'Vui lòng chọn phương thức thanh toán')
                return redirect('bookings:payment', ticket_id='preview')

            try:
                # Lấy tour_id và tìm tour trực tiếp
                from tours.models import Tour
                try:
                    tour_id = int(preview_data['tour_id'])
                    tour = Tour.objects.get(tour_id=tour_id, is_active=True)
                except (ValueError, TypeError, KeyError, Tour.DoesNotExist):
                    messages.error(request, 'Thông tin tour không hợp lệ')
                    return redirect('bookings:booking_list')

                # Tìm package (nếu có) - không bắt buộc
                package = None
                package_id = preview_data.get('package_id')
                if package_id:
                    try:
                        package_id = int(package_id)
                        package = Package.objects.filter(id=package_id).first()
                        # Nếu package không tồn tại hoặc không active, vẫn cho phép nhưng không dùng package
                        if package and not package.is_active:
                            package = None
                    except (ValueError, TypeError):
                        package = None

                # Tạo booking (package có thể là None)
                booking = BookingService.create_booking(
                    user=request.user,
                    booking_type='tour',
                    number_of_people=preview_data['number_of_people'],
                    total_price=preview_data['total_cost'],
                    package=package  # Có thể là None nếu không có package
                )

                # Tạo vé
                ticket = Ticket.objects.create(
                    booking=booking,
                    passenger_name=preview_data['passenger_name'],
                    flight_details=preview_data.get('flight_details', f"Tour: {preview_data['tour_name']}\nĐiểm đến: {preview_data['destination_name']}"),
                    hotel_room_details="Tour không bao gồm khách sạn",
                    total_cost=preview_data['total_cost'],
                    payment_method=payment_method
                )

                # Cập nhật trạng thái booking
                booking.status = 'paid'
                booking.save()

                # Update preview in session instead of deleting so user returning to preview
                # sees the paid status. Also store payment method for display.
                preview_data['booking_status'] = 'paid'
                preview_data['payment_method'] = payment_method
                # Store the real ticket id so the preview can display it
                try:
                    preview_data['ticket_id'] = int(ticket.ticket_id)
                except Exception:
                    preview_data['ticket_id'] = str(ticket.ticket_id)
                try:
                    preview_data['total_cost'] = float(preview_data.get('total_cost', ticket.total_cost))
                except Exception:
                    preview_data['total_cost'] = ticket.total_cost

                request.session['ticket_preview'] = preview_data
                request.session.modified = True

                messages.success(request, f'Thanh toán thành công! Mã vé: {ticket.ticket_id}')
                # Redirect back to preview ticket so the preview page shows updated paid state
                return redirect('bookings:ticket_detail', ticket_id='preview')

            except Exception as e:
                messages.error(request, f'Lỗi khi tạo vé: {str(e)}')
                return redirect('bookings:booking_list')

        # GET request - hiển thị form thanh toán
        user_name = request.user.get_full_name() or request.user.username if request.user.is_authenticated else preview_data.get('passenger_name', '')
        user_phone = getattr(request.user, 'phone_number', 'N/A') if request.user.is_authenticated else ''

        # Tạo QR code random
        qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        # Số tài khoản ảo random
        account_number = ''.join(random.choices(string.digits, k=13))

        # Tạo ticket preview object cho template
        class PreviewTicket:
            def __init__(self, data):
                # If a real ticket was created during payment, show its id
                self.ticket_id = data.get('ticket_id', 'preview')
                self.passenger_name = data['passenger_name']
                self.total_cost = data['total_cost']
                self.tour_name = data.get('tour_name', 'Tour')
                self.destination_name = data.get('destination_name', '')

        preview_ticket = PreviewTicket(preview_data)

        context = {
            'ticket': preview_ticket,
            'preview_data': preview_data,
            'user_name': user_name,
            'user_phone': user_phone,
            'qr_code': qr_code,
            'account_number': account_number,
            'is_preview': True
        }

        return render(request, 'payment.html', context)

    else:
        # Thanh toán cho vé thật (nếu cần)
        ticket = get_object_or_404(Ticket, ticket_id=ticket_id, booking__user=request.user)

        if request.method == 'POST':
            # Xác nhận thanh toán
            ticket.booking.status = 'paid'
            ticket.booking.save()
            ticket.payment_method = request.POST.get('payment_method', 'banking')
            ticket.save()
            messages.success(request, 'Thanh toán thành công! Trạng thái booking đã được cập nhật.')
            return redirect('bookings:ticket_detail', ticket_id=ticket.ticket_id)

        # Thông tin người dùng
        user_name = request.user.get_full_name() or request.user.username
        user_phone = getattr(request.user, 'phone_number', 'N/A')

        # Tạo QR code random
        qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

        # Số tài khoản ảo random
        account_number = ''.join(random.choices(string.digits, k=13))

        context = {
            'ticket': ticket,
            'user_name': user_name,
            'user_phone': user_phone,
            'qr_code': qr_code,
            'account_number': account_number,
            'is_preview': False
        }

        return render(request, 'payment.html', context)


def create_ticket_from_tour(request):
    if request.method != 'POST':
        return redirect('tours:tour_list')

    try:
        tour_id = request.POST.get('tour_id')
        package_id = request.POST.get('package_id')
        number_of_people = int(request.POST.get('number_of_people', 1))
        passenger_name = request.POST.get('name', request.user.get_full_name() or request.user.username if request.user.is_authenticated else '')
        email = request.POST.get('email', request.user.email if request.user.is_authenticated else '')

        if not tour_id:
            messages.error(request, 'Thiếu thông tin tour')
            return redirect('tours:tour_list')

        # Tìm tour
        from tours.models import Tour
        try:
            tour = Tour.objects.get(tour_id=tour_id, is_active=True)
        except Tour.DoesNotExist:
            messages.error(request, 'Tour không tồn tại hoặc không khả dụng')
            return redirect('tours:tour_list')

        # Tính tổng giá
        base_price = tour.price
        if package_id:
            try:
                package = Package.objects.get(id=int(package_id), is_active=True)
                total_cost = (base_price + package.price) * number_of_people
                package_name = package.name
            except (ValueError, Package.DoesNotExist):
                total_cost = base_price * number_of_people
                package_name = None
        else:
            total_cost = base_price * number_of_people
            package_name = None

        # Tạo preview data
        preview_data = {
            'tour_id': tour_id,
            'tour_name': tour.name,
            'destination_name': tour.location,
            'package_id': package_id if package_id else None,
            'package_name': package_name,
            'number_of_people': number_of_people,
            'total_cost': float(total_cost),
            'passenger_name': passenger_name,
            'email': email,
            'flight_details': f"Tour: {tour.name}\nĐiểm đến: {tour.location}",
        }

        # Lưu vào session
        request.session['ticket_preview'] = preview_data

        messages.success(request, 'Đã tạo vé xem trước thành công')
        return redirect('bookings:ticket_detail', ticket_id='preview')

    except Exception as e:
        messages.error(request, f'Lỗi khi tạo vé: {str(e)}')
        return redirect('tours:tour_list')
