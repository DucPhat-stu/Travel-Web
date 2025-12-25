from rest_framework import serializers
from .models import Tour


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Giá phải lớn hơn hoặc bằng 0")
        return value

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Số ngày phải lớn hơn 0")
        return value
