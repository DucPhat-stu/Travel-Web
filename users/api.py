from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .permissions import IsAdminOrSelf, IsAdminOrReadOnly
from .serializers import UserSerializer, UserCreateSerializer, UserLoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD user cho admin, user thường chỉ xem/sửa chính mình.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, "is_admin", False):
            return User.objects.all()
        return User.objects.filter(pk=getattr(user, "pk", None))


class ObtainAPITokenView(APIView):
    """
    Đăng nhập và nhận token API.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Thu hồi token cũ và cấp token mới
        UserTokenAuthentication.revoke_user_tokens(user)
        token = UserTokenAuthentication.issue_token(user)

        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )

