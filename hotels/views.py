from django.shortcuts import render, get_object_or_404
from .models import Hotel

def hotel_list(request):
    hotels = Hotel.objects.filter(is_active=True)
    return render(request, 'hotels.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id, is_active=True)
    return render(request, 'hotel-details.html', {'hotel': hotel})
