from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Cho phép đọc với tất cả, chỉ admin mới được sửa.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = getattr(request, "user", None)
        return bool(user and getattr(user, "is_admin", False))


class IsAdminOrSelf(permissions.BasePermission):
    """
    User thường chỉ được xem/sửa chính mình, admin có toàn quyền.
    """

    def has_object_permission(self, request, view, obj):
        user = getattr(request, "user", None)
        if not user:
            return False
        if getattr(user, "is_admin", False):
            return True
        return obj == user

    def has_permission(self, request, view):
        if view.action == "create":
            return True  # Cho phép đăng ký
        return request.user and request.user.is_authenticated

