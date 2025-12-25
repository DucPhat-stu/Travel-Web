from django.db import models
from django.utils import timezone

class ChatMessage(models.Model):
    """
    Model quản lý tin nhắn chatbot
    """
    message_id = models.AutoField(primary_key=True)
    user_message = models.TextField(verbose_name="Tin nhắn người dùng")
    bot_response = models.TextField(verbose_name="Phản hồi bot")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo")

    class Meta:
        db_table = 'chatbot_chatmessage'
        verbose_name = "Tin nhắn Chatbot"
        verbose_name_plural = "Tin nhắn Chatbot"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message {self.message_id}"
