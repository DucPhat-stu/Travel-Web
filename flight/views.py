from django.shortcuts import render, get_object_or_404
from .models import Flight

def flight_list(request):
    flights = Flight.objects.filter(is_active=True)
    return render(request, 'flight.html', {'flights': flights})

def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, flight_id=flight_id, is_active=True)
    return render(request, 'flight-details.html', {'flight': flight})
