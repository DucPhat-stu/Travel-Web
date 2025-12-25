"""
Service layer cho booking
Xử lý logic gợi ý vé máy bay, khách sạn dựa trên tiêu chí người dùng
"""

from decimal import Decimal
from django.db.models import Q
from flight.models import Flight
from hotels.models import Hotel
from tours.models import Tour
from .models import Booking


class BookingRecommendationService:
    """
    Service gợi ý vé máy bay và khách sạn dựa trên:
    - Nơi muốn đi
    - Số ngày
    - Chi phí hiện có
    - Loại khách sạn
    """
    
    # Giá vé máy bay mẫu (VND)
    FLIGHT_PRICES = {
        'paris': 15000000,
        'tokyo': 18000000,
        'bali': 8000000,
        'bangkok': 5000000,
        'singapore': 6000000,
        'dubai': 12000000,
        'new_york': 20000000,
        'london': 16000000,
        'sydney': 22000000,
        'hanoi': 2000000,
        'hcm': 2000000,
        'danang': 1500000,
    }
    
    # Giá khách sạn mẫu theo sao (VND/đêm)
    HOTEL_PRICES = {
        '3': {
            'min': 1000000,
            'max': 2000000,
            'avg': 1500000
        },
        '4': {
            'min': 2000000,
            'max': 4000000,
            'avg': 3000000
        },
        '5': {
            'min': 4000000,
            'max': 8000000,
            'avg': 6000000
        }
    }
    
    @staticmethod
    def get_flight_recommendations(destination, number_of_people, budget):
        """
        Lấy gợi ý vé máy bay
        
        Args:
            destination: Điểm đến
            number_of_people: Số người
            budget: Chi phí hiện có
        
        Returns:
            dict: Thông tin vé máy bay gợi ý
        """
        # Tính giá vé cho mỗi người
        base_price = BookingRecommendationService.FLIGHT_PRICES.get(destination, 10000000)
        price_per_person = base_price
        total_flight_price = price_per_person * number_of_people
        
        # Kiểm tra xem có đủ tiền cho vé máy bay không
        can_afford = total_flight_price <= budget
        
        # Tính phần trăm chi phí
        percentage = (total_flight_price / budget * 100) if budget > 0 else 0
        
        return {
            'destination': destination,
            'price_per_person': price_per_person,
            'total_price': total_flight_price,
            'number_of_people': number_of_people,
            'can_afford': can_afford,
            'percentage_of_budget': round(percentage, 2),
            'remaining_budget': budget - total_flight_price if can_afford else 0
        }
    
    @staticmethod
    def get_hotel_recommendations(destination, number_of_days, number_of_people, 
                                  remaining_budget, hotel_star=None):
        """
        Lấy gợi ý khách sạn
        
        Args:
            destination: Điểm đến
            number_of_days: Số ngày
            number_of_people: Số người
            remaining_budget: Chi phí còn lại sau vé máy bay
            hotel_star: Loại khách sạn (3, 4, 5 sao)
        
        Returns:
            list: Danh sách khách sạn gợi ý
        """
        recommendations = []
        
        # Nếu không chỉ định loại khách sạn, gợi ý tất cả
        stars = [hotel_star] if hotel_star else ['3', '4', '5']
        
        for star in stars:
            if star not in BookingRecommendationService.HOTEL_PRICES:
                continue
            
            prices = BookingRecommendationService.HOTEL_PRICES[star]
            
            # Tính giá phòng cho mỗi đêm
            # Giả sử 1 phòng cho 2 người
            rooms_needed = (number_of_people + 1) // 2
            
            # Tính giá trung bình
            avg_price_per_room = prices['avg']
            total_hotel_price = avg_price_per_room * rooms_needed * number_of_days
            
            # Kiểm tra xem có đủ tiền không
            can_afford = total_hotel_price <= remaining_budget
            
            # Tính phần trăm chi phí
            percentage = (total_hotel_price / remaining_budget * 100) if remaining_budget > 0 else 0
            
            recommendations.append({
                'star': star,
                'rooms_needed': rooms_needed,
                'price_per_room_per_night': avg_price_per_room,
                'total_price': total_hotel_price,
                'number_of_nights': number_of_days,
                'can_afford': can_afford,
                'percentage_of_remaining_budget': round(percentage, 2),
                'final_remaining_budget': remaining_budget - total_hotel_price if can_afford else 0
            })
        
        # Sắp xếp theo giá từ thấp đến cao
        recommendations.sort(key=lambda x: x['total_price'])
        
        return recommendations
    
    @staticmethod
    def get_complete_recommendation(destination, number_of_days, number_of_people, 
                                   budget, hotel_star=None):
        """
        Lấy gợi ý hoàn chỉnh (vé máy bay + khách sạn)
        
        Args:
            destination: Điểm đến
            number_of_days: Số ngày
            number_of_people: Số người
            budget: Chi phí hiện có
            hotel_star: Loại khách sạn (tùy chọn)
        
        Returns:
            dict: Gợi ý hoàn chỉnh
        """
        # Lấy gợi ý vé máy bay
        flight_rec = BookingRecommendationService.get_flight_recommendations(
            destination, number_of_people, budget
        )
        
        # Lấy gợi ý khách sạn
        remaining_budget = flight_rec['remaining_budget']
        hotel_recs = BookingRecommendationService.get_hotel_recommendations(
            destination, number_of_days, number_of_people, remaining_budget, hotel_star
        )
        
        return {
            'flight': flight_rec,
            'hotels': hotel_recs,
            'total_budget': budget,
            'total_cost': flight_rec['total_price'] + (hotel_recs[0]['total_price'] if hotel_recs else 0),
            'is_affordable': flight_rec['can_afford'] and (hotel_recs[0]['can_afford'] if hotel_recs else False)
        }
    
    @staticmethod
    def calculate_booking_cost(flight_price, hotel_price, number_of_people):
        """
        Tính tổng chi phí booking
        
        Args:
            flight_price: Giá vé máy bay
            hotel_price: Giá khách sạn
            number_of_people: Số người
        
        Returns:
            Decimal: Tổng chi phí
        """
        return Decimal(str(flight_price + hotel_price))


class BookingService:
    """
    Service quản lý booking
    """
    
    @staticmethod
    def create_booking(user, booking_type, number_of_people, total_price, 
                      tour=None, hotel=None, flight=None, package=None):
        """
        Tạo booking mới
        
        Args:
            user: User object
            booking_type: Loại booking (tour, hotel, flight)
            number_of_people: Số người
            total_price: Tổng giá
            tour: Tour object (tùy chọn)
            hotel: Hotel object (tùy chọn)
            flight: Flight object (tùy chọn)
            package: Package object (tùy chọn)
        
        Returns:
            Booking: Booking object được tạo
        """
        from django.utils import timezone
        
        booking = Booking(
            user=user,
            booking_type=booking_type,
            number_of_people=number_of_people,
            total_price=total_price,
            tour=tour,
            hotel=hotel,
            flight=flight,
            package=package,
            booking_date=timezone.now().date()
        )
        booking.save()
        return booking
    
    @staticmethod
    def get_user_bookings(user):
        """
        Lấy tất cả booking của user
        
        Args:
            user: User object
        
        Returns:
            QuerySet: Danh sách booking
        """
        return Booking.objects.filter(user=user, is_active=True).order_by('-created_at')
    
    @staticmethod
    def cancel_booking(booking):
        """
        Hủy booking
        
        Args:
            booking: Booking object
        
        Returns:
            bool: True nếu thành công
        """
        booking.is_active = False
        booking.save()
        return True
    
    @staticmethod
    def get_booking_details(booking_id):
        """
        Lấy chi tiết booking
        
        Args:
            booking_id: ID của booking
        
        Returns:
            Booking: Booking object
        """
        try:
            return Booking.objects.get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return None
