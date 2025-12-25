from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, timedelta

from users.permissions import IsAdminOrReadOnly
from tours.models import Tour
from hotels.models import Hotel
from flight.models import Flight

from .models import Destination, Package, Review, Comment
from .serializers import (
    DestinationSerializer,
    PackageSerializer,
    ReviewSerializer,
    CommentSerializer,
    PlannerSearchSerializer,
    TripQuoteSerializer,
)
from .models import AirlineFareRule, VisaRequirement


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.filter(is_active=True)
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.filter(is_active=True).select_related("destination").prefetch_related(
        "tours", "hotels", "flights"
    )
    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("user", "content_type")
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("user", "review")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlannerSearchView(APIView):
    """
    Nhận yêu cầu từ form kế hoạch và trả về gợi ý tour/hotel/flight + packages.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = PlannerSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        dest_query = data.get("destination", "")
        tour_type = data.get("tour_type", "")
        budget_min = data.get("budget_min")
        budget_max = data.get("budget_max")
        label = data.get("label", "")
        min_rooms = data.get("min_rooms_available")
        min_seats = data.get("min_seats_available")

        destinations = Destination.objects.filter(is_active=True)
        if dest_query:
            destinations = destinations.filter(
                Q(name__icontains=dest_query) | Q(region__icontains=dest_query) | Q(country__icontains=dest_query)
            )

        tours = Tour.objects.filter(is_active=True)
        hotels = Hotel.objects.filter(is_active=True)
        flights = Flight.objects.filter(is_active=True)

        if dest_query:
            tours = tours.filter(Q(location__icontains=dest_query) | Q(name__icontains=dest_query))
            hotels = hotels.filter(Q(location__icontains=dest_query) | Q(name__icontains=dest_query))
            flights = flights.filter(Q(destination__icontains=dest_query) | Q(departure__icontains=dest_query))

        if tour_type:
            tours = tours.filter(description__icontains=tour_type)

        if min_rooms is not None:
            hotels = hotels.filter(rooms_available__gte=min_rooms)
        if min_seats is not None:
            flights = flights.filter(seats_available__gte=min_seats)

        packages = Package.objects.filter(is_active=True)
        if destinations.exists():
            packages = packages.filter(destination__in=destinations)
        if label:
            packages = packages.filter(label=label)
        if budget_min is not None:
            packages = packages.filter(base_price__gte=budget_min)
        if budget_max is not None:
            packages = packages.filter(base_price__lte=budget_max)
        if min_rooms is not None:
            packages = packages.filter(hotels__rooms_available__gte=min_rooms)
        if min_seats is not None:
            packages = packages.filter(flights__seats_available__gte=min_seats)
        packages = packages.distinct()

        response = {
            "destinations": DestinationSerializer(destinations[:10], many=True).data,
            "packages": PackageSerializer(packages[:10], many=True).data,
            "tours": [],  # fallback nếu không có package phù hợp
            "hotels": [],
            "flights": [],
        }

        if not packages.exists():
            response["tours"] = [
                {
                    "id": t.pk,
                    "name": t.name,
                    "price": t.price,
                    "location": t.location,
                    "duration": t.duration,
                    "image": t.image.url if t.image else None,
                }
                for t in tours[:10]
            ]
            response["hotels"] = [
                {
                    "id": h.pk,
                    "name": h.name,
                    "price": h.price,
                    "location": h.location,
                    "rooms_available": getattr(h, "rooms_available", None),
                    "image": h.image.url if h.image else None,
                }
                for h in hotels[:10]
            ]
            response["flights"] = [
                {
                    "id": f.pk,
                    "flight_number": f.flight_number,
                    "departure": f.departure,
                    "destination": f.destination,
                    "price": f.price,
                    "departure_time": f.departure_time,
                    "seats_available": getattr(f, "seats_available", None),
                }
                for f in flights[:10]
            ]

        return Response(response, status=status.HTTP_200_OK)


class TripQuoteView(APIView):
    """
    Nhận thông tin chuyến đi, tính giá vé (oneway/khứ hồi), giá khách sạn và gợi ý budget.
    Logic nội bộ, không gọi API ngoài.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = TripQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        carrier = data["carrier"]
        departure = data["departure"]
        destination = data["destination"]
        trip_type = data["trip_type"]
        depart_date = data["depart_date"]
        return_date = data.get("return_date")
        adults = data.get("adults", 1)
        children = data.get("children", 0)
        hotel_id = data.get("hotel_id")
        checkin = data.get("checkin")
        checkout = data.get("checkout")
        rooms = data.get("rooms", 1)
        passport_no = data.get("passport_no") or ""
        passport_expiry = data.get("passport_expiry")
        has_visa = data.get("has_visa", False)
        nationality = data.get("nationality") or ""

        # Xác định domestic/international đơn giản: country strings trong departure/destination
        def is_domestic(dep, dest):
            return dep.lower().strip().endswith("vietnam") or dep.lower().startswith("vn") and dest.lower().strip().endswith("vietnam")

        route_type = "domestic" if is_domestic(departure, destination) else "international"

        # Passport/visa check (nội bộ)
        warnings = []
        if route_type == "international":
            if not passport_no:
                warnings.append("Cần nhập số hộ chiếu cho chuyến quốc tế.")
            if passport_expiry:
                min_valid = depart_date + timedelta(days=180)
                if passport_expiry < min_valid:
                    warnings.append("Hộ chiếu hết hạn/không đủ 6 tháng tính từ ngày đi.")
            else:
                warnings.append("Chưa có ngày hết hạn hộ chiếu.")

            visa_req = VisaRequirement.objects.filter(country_code__iexact=destination[:2]).first()
            if visa_req and visa_req.visa_required and not has_visa:
                warnings.append("Chưa có visa cho quốc gia đích.")

        # Quote flight
        rule = AirlineFareRule.objects.filter(
            carrier=carrier, route_type=route_type, trip_type=trip_type, is_active=True
        ).first()

        if not rule:
            return Response(
                {"detail": "Chưa có bảng giá cho hãng/tuyến này. Vui lòng cấu hình AirlineFareRule."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        days_diff = max((depart_date - date.today()).days, 0)
        flight_price = float(rule.base_price) * (1 + float(rule.multiplier_advance) * days_diff)
        legs = 2 if trip_type == "roundtrip" and return_date else 1
        flight_price = flight_price * legs + float(rule.tax_fee)
        # nhân theo hành khách (trẻ em có thể giảm, tạm 75%)
        passengers_total = adults + 0.75 * children
        flight_total = flight_price * passengers_total

        # Quote hotel (mock realtime)
        hotel_total = 0
        hotel_nights = 0
        hotel_price_per_night = None
        if hotel_id and checkin and checkout:
            hotel = Hotel.objects.filter(pk=hotel_id).first()
            if not hotel:
                return Response({"detail": "Hotel không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
            hotel_price_per_night = float(hotel.price)
            hotel_nights = max((checkout - checkin).days, 0)
            hotel_total = hotel_price_per_night * hotel_nights * rooms

        budget_min = (flight_total + hotel_total) * 1.1

        return Response(
            {
                "route_type": route_type,
                "flight": {
                    "carrier": carrier,
                    "trip_type": trip_type,
                    "legs": legs,
                    "base_price_rule": float(rule.base_price),
                    "multiplier_advance": float(rule.multiplier_advance),
                    "tax_fee": float(rule.tax_fee),
                    "passengers_equivalent": passengers_total,
                    "total": round(flight_total, 2),
                },
                "hotel": {
                    "hotel_id": hotel_id,
                    "price_per_night": hotel_price_per_night,
                    "nights": hotel_nights,
                    "rooms": rooms,
                    "total": round(hotel_total, 2),
                },
                "budget_min_suggest": round(budget_min, 2),
                "warnings": warnings,
            },
            status=status.HTTP_200_OK,
        )

