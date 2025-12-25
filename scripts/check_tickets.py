import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from bookings.models import Booking, Ticket

print('Bookings (paid) count:', Booking.objects.filter(status='paid').count())
print('Tickets count:', Ticket.objects.count())
for t in Ticket.objects.order_by('-created_at')[:5]:
    print(t.ticket_id, t.passenger_name, t.total_cost, t.payment_method, t.booking.status)
