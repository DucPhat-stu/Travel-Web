#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from tours.models import Tour
from django.utils import timezone

# Create multiple tours
tours_data = [
    (1001, 'Ha Long 3N2Đ', 'Tham quan vịnh, ngủ đêm trên tàu', 450.00, 3, 'Quang Ninh'),
    (1002, 'Bà Nà Hills 1N', 'Check-in Cầu Vàng, vườn hoa', 120.00, 1, 'Da Nang'),
    (1003, 'Sapa Trekking 2N1Đ', 'Chinh phục đỉnh Fansipan', 250.00, 2, 'Lao Cai'),
    (1004, 'Phú Quốc Resort 4N3Đ', 'Nghỉ dưỡng tại Phú Quốc', 650.00, 4, 'Kien Giang'),
    (1005, 'Nha Trang Beach 3N2Đ', 'Biển xanh và hải sản tươi', 420.00, 3, 'Khanh Hoa'),
    (1006, 'Đà Lạt Flower City 2N1Đ', 'Thành phố ngàn hoa', 350.00, 2, 'Lam Dong'),
    (1007, 'Hội An Ancient Town 2N1Đ', 'Di sản văn hóa thế giới', 380.00, 2, 'Quang Nam'),
    (1008, 'Cần Thơ Mekong Delta 1N', 'Du lịch miền Tây sông nước', 280.00, 1, 'Can Tho'),
    (1009, 'Vũng Tàu Beach 2N1Đ', 'Biển Vũng Tàu và hải sản', 320.00, 2, 'Ba Ria Vung Tau'),
    (1010, 'Hà Nội Old Quarter 2N1Đ', 'Khám phá phố cổ Hà Nội', 280.00, 2, 'Ha Noi'),
    (1011, 'Hồ Chí Minh City Tour 3N2Đ', 'Thành phố Sài Gòn năng động', 400.00, 3, 'Ho Chi Minh City'),
    (1012, 'Mũi Né Beach 2N1Đ', 'Biển xanh cát vàng', 350.00, 2, 'Binh Thuan'),
    (1013, 'Phong Nha Caves 2N1Đ', 'Hang động kỳ quan thế giới', 480.00, 2, 'Quang Binh'),
    (1014, 'Côn Đảo Islands 3N2Đ', 'Quần đảo xanh', 550.00, 3, 'Ba Ria Vung Tau'),
    (1015, 'Tam Đảo Mountain 1N', 'Núi rừng xanh mát', 180.00, 1, 'Vinh Phuc'),
    (1016, 'Mai Châu Valley 2N1Đ', 'Thung lũng xanh', 320.00, 2, 'Hoa Binh'),
    (1017, 'Hà Giang Loop 4N3Đ', 'Đèo cao vực sâu', 600.00, 4, 'Ha Giang'),
    (1018, 'Quy Nhơn Beach 3N2Đ', 'Biển xanh Eo Gió', 420.00, 3, 'Binh Dinh'),
    (1019, 'Buôn Ma Thuột 2N1Đ', 'Thành phố cà phê', 380.00, 2, 'Dak Lak'),
]

for tour_id, name, description, price, duration, location in tours_data:
    tour, created = Tour.objects.get_or_create(
        tour_id=tour_id,
        defaults={
            'name': name,
            'description': description,
            'price': price,
            'duration': duration,
            'location': location,
            'is_active': True,
        }
    )
    if created:
        print(f'Tour created: {tour.name} (ID: {tour.tour_id})')
    else:
        print(f'Tour already exists: {tour.name} (ID: {tour.tour_id})')
