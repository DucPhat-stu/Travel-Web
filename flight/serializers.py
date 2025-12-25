from rest_framework import serializers

from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Giá phải lớn hơn hoặc bằng 0")
        return value

    def validate(self, attrs):
        departure_time = attrs.get("departure_time")
        arrival_time = attrs.get("arrival_time")
        if departure_time and arrival_time and arrival_time <= departure_time:
            raise serializers.ValidationError("Thời gian đến phải sau thời gian khởi hành")
        return attrs

