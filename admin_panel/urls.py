from django.urls import path
from django.http import HttpResponse

app_name = 'admin_panel'

# Temporary view until admin_panel views are created
def placeholder(request):
    return HttpResponse("Admin Panel - Coming Soon")

urlpatterns = [
    path('', placeholder, name='dashboard'),
]

