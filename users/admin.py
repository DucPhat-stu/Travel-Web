from django.contrib import admin
from .models import User, UserToken

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    # Cấu hình hiển thị User trong Django Admin
    
    list_display = [
        'user_id',
        'email',
        'full_name',
        'phone',
        'role',
        'is_active',
        'created_at'
    ]

    list_filter = ['role', 'is_active', 'created_at']

    search_fields = ['email', 'full_name', 'phone']

    readonly_fields = ['user_id', 'created_at', 'updated_at', 'password']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('user_id', 'full_name', 'email', 'phone', 'address')
        }),
        ('Phân quyền', {
            'fields': ('role', 'is_active')
        }),
        ('Bảo mật', {
            'fields': ('password', 'reset_token', 'reset_token_expiry'),
            'classes': ('collapse',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    ordering = ['-created_at']

    def has_delete_permission(self, request, obj=None):

        return request.user.is_superuser


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ["key", "user", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["key", "user__email"]
