import logging

from app.models import User
from app.serializers.user_serializers import (
    UserCreateSerializer,
    UserListSerializer,
    UserUpdateSerializer,
)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)

from datetime import datetime

logger = logging.getLogger('view')


# Views
class UserRegisterView(CreateAPIView):
    """
    ** View to register user **
    """
    permission_classes = (AllowAny, )
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = True
        return super().create(request, *args, **kwargs)


class UserLogoutView(APIView):
    """
    ** View to logout active user **
    """
    permission_classes = (AllowAny, )
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            user.is_active = False
            user.save()
            return Response({"detail": f"User {user} logged out!"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("User logout error :: ", e)
            return Response({"detail": "Error while logging out user."}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(ListAPIView):
    """
    ** View to list all users detail **
    """
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    ** View to retrieve, update and delete specific user detail using uuid **
    """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return UserUpdateSerializer
        else:
            return UserListSerializer

    def put(self, request, *args, **kwargs):
        request.data["updated_at"] = datetime.now()
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        request.data["updated_at"] = datetime.now()
        return super().partial_update(request, *args, **kwargs)
    

