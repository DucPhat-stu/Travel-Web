from rest_framework import serializers

from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = "__all__"
        read_only_fields = ["message_id", "created_at"]

    def validate(self, attrs):
        if not attrs.get("user_message"):
            raise serializers.ValidationError("Tin nhắn người dùng không được để trống")
        if not attrs.get("bot_response"):
            raise serializers.ValidationError("Phản hồi bot không được để trống")
        return attrs

