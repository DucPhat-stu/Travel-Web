from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["booking_id", "created_at", "updated_at", "user"]

    def validate(self, attrs):
        booking_type = attrs.get("booking_type")
        tour = attrs.get("tour")
        hotel = attrs.get("hotel")
        flight = attrs.get("flight")
        package = attrs.get("package")
        total_price = attrs.get("total_price")
        number_of_people = attrs.get("number_of_people")

        if booking_type == "tour" and not tour:
            raise serializers.ValidationError("Phải chọn tour khi booking_type = tour")
        if booking_type == "hotel" and not hotel:
            raise serializers.ValidationError("Phải chọn hotel khi booking_type = hotel")
        if booking_type == "flight" and not flight:
            raise serializers.ValidationError("Phải chọn flight khi booking_type = flight")

        if package and not booking_type:
            raise serializers.ValidationError("Nếu chọn package, cần set booking_type tương ứng")

        if total_price is not None and total_price < 0:
            raise serializers.ValidationError("Tổng giá phải lớn hơn hoặc bằng 0")
        if number_of_people is not None and number_of_people <= 0:
            raise serializers.ValidationError("Số người phải lớn hơn 0")

        return attrs
