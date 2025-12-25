from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from .models import Destination, Package, Review, Comment
from tours.serializers import TourSerializer
from hotels.serializers import HotelSerializer
from flight.serializers import FlightSerializer


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = "__all__"


class PackageSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(), write_only=True, source="destination"
    )
    tours = TourSerializer(many=True, read_only=True)
    hotels = HotelSerializer(many=True, read_only=True)
    flights = FlightSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = [
            "id",
            "title",
            "description",
            "base_price",
            "label",
            "rating_cached",
            "is_active",
            "destination",
            "destination_id",
            "tours",
            "hotels",
            "flights",
            "created_at",
            "updated_at",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    target_label = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "user_email",
            "content_type",
            "object_id",
            "rating",
            "comment",
            "status",
            "target_label",
            "created_at",
        ]
        read_only_fields = ["status", "created_at"]

    def get_target_label(self, obj):
        return f"{obj.content_type.app_label}.{obj.content_type.model}:{obj.object_id}"

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating phải từ 1 đến 5")
        return value


class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "user_email", "review", "content", "status", "created_at"]
        read_only_fields = ["status", "created_at"]


class PlannerSearchSerializer(serializers.Serializer):
    destination = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    adults = serializers.IntegerField(required=False, min_value=1, default=1)
    children = serializers.IntegerField(required=False, min_value=0, default=0)
    tour_type = serializers.CharField(required=False, allow_blank=True)
    budget_min = serializers.DecimalField(required=False, max_digits=12, decimal_places=2)
    budget_max = serializers.DecimalField(required=False, max_digits=12, decimal_places=2)
    label = serializers.CharField(required=False, allow_blank=True)
    min_rooms_available = serializers.IntegerField(required=False, min_value=0)
    min_seats_available = serializers.IntegerField(required=False, min_value=0)


class TripQuoteSerializer(serializers.Serializer):
    carrier = serializers.ChoiceField(choices=["vietjet", "bamboo", "vna", "viettravel"])
    departure = serializers.CharField()
    destination = serializers.CharField()
    trip_type = serializers.ChoiceField(choices=["oneway", "roundtrip"])
    depart_date = serializers.DateField()
    return_date = serializers.DateField(required=False)
    adults = serializers.IntegerField(min_value=1, default=1)
    children = serializers.IntegerField(min_value=0, default=0)
    hotel_id = serializers.IntegerField(required=False)
    checkin = serializers.DateField(required=False)
    checkout = serializers.DateField(required=False)
    rooms = serializers.IntegerField(required=False, min_value=1, default=1)
    passport_no = serializers.CharField(required=False, allow_blank=True)
    passport_expiry = serializers.DateField(required=False)
    has_visa = serializers.BooleanField(required=False, default=False)
    nationality = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        trip_type = attrs.get("trip_type")
        return_date = attrs.get("return_date")
        depart_date = attrs.get("depart_date")
        checkin = attrs.get("checkin")
        checkout = attrs.get("checkout")

        if trip_type == "roundtrip" and not return_date:
            raise serializers.ValidationError("Khứ hồi cần nhập ngày về")
        if return_date and depart_date and return_date < depart_date:
            raise serializers.ValidationError("Ngày về phải sau ngày đi")
        if checkin and checkout and checkout <= checkin:
            raise serializers.ValidationError("Checkout phải sau checkin")
        return attrs

