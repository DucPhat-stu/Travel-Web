from rest_framework import serializers

from .models import User
from .services import UserService


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "full_name",
            "email",
            "phone",
            "address",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user_id", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["full_name", "email", "phone", "address", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email đã được sử dụng")
        return value

    def create(self, validated_data):
        # Sử dụng service để đảm bảo đồng nhất logic hash password
        return UserService.create_user(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            password=validated_data["password"],
            address=validated_data.get("address", ""),
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from .services import UserService

        user = UserService.authenticate_user(
            email=attrs.get("email"), password=attrs.get("password")
        )
        if not user:
            raise serializers.ValidationError("Email hoặc mật khẩu không đúng")
        attrs["user"] = user
        return attrs

