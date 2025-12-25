from django.test import Client
from users.models import User
from bookings.models import Booking, Ticket

c = Client()
user = User.objects.filter(email='user@travel.com').first()
if not user:
    raise SystemExit('Test user not found')

c.force_login(user)
# Prepare preview in session
s = c.session
s['ticket_preview'] = {
    'tour_id': '1009',
    'tour_name': 'Vũng Tàu Beach 2N1Đ',
    'destination_name': 'Ba Ria Vung Tau',
    'number_of_people': 1,
    'total_cost': 320.0,
    'passenger_name': 'Test User',
    'email': 'user@travel.com'
}
s.save()

# POST payment
r = c.post('/bookings/payment/preview/', {'payment_method': 'banking'}, follow=True)
content = r.content.decode('utf-8')
with open('scripts/preview_django_client.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Status', r.status_code)
print('Redirects', r.redirect_chain)
print('Bookings count', Booking.objects.count())
print('Tickets count', Ticket.objects.count())
print('Paid bookings', Booking.objects.filter(status='paid').count())
print('Preview contains paid?', 'Đã thanh toán' in content)
print('Saved to scripts/preview_django_client.html')
