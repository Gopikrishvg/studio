from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model, login, logout
from accounts.models import Profile, Event, Studio
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserLoginSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    EventSerializer,
    StudioSerializer,
    MemberSerializer,
)

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            login(request, user)
            data = {
                'id': user.id,
                'is_staff':user.is_staff,


                'is_admin':user.is_admin,
                "token": jwt_encode_handler(jwt_payload_handler(user)),  }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PasswordChangeView(UpdateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class=PasswordResetSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProfileListCreateView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class ProfileRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class MemberRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class EventRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class StudioListCreateView(ListCreateAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class StudioRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
