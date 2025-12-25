import secrets
from typing import Optional, Tuple

from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header

from .models import UserToken, User


class UserTokenAuthentication(authentication.BaseAuthentication):
    """
    Xác thực API sử dụng header Authorization: Token <key>.
    """

    keyword = b"token"

    def authenticate(self, request) -> Optional[Tuple[User, UserToken]]:
        auth = get_authorization_header(request).split()

        if not auth:
            return None

        if auth[0].lower() != self.keyword:
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed(_("Thiếu token"))
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed(_("Token không hợp lệ"))

        try:
            key = auth[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed(_("Token chứa ký tự không hợp lệ"))

        return self.authenticate_credentials(key)

    def authenticate_credentials(self, key: str) -> Tuple[User, UserToken]:
        try:
            token = UserToken.objects.select_related("user").get(key=key, is_active=True)
        except UserToken.DoesNotExist:
            raise exceptions.AuthenticationFailed(_("Token không hợp lệ hoặc đã hết hạn"))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_("Tài khoản đã bị khóa"))

        return (token.user, token)

    @staticmethod
    def issue_token(user: User) -> UserToken:
        """
        Tạo token mới cho user, vô hiệu hóa token cũ nếu cần.
        """
        token = UserToken(user=user, key=secrets.token_hex(20), is_active=True)
        token.save()
        return token

    @staticmethod
    def revoke_user_tokens(user: User) -> None:
        UserToken.objects.filter(user=user, is_active=True).update(is_active=False)

