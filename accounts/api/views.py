from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model, login, logout
from accounts.models import Profile, Event, Studio, StudioImage, StudioVideo
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserLoginSerializer,
    ProfileSerializer,
    EventSerializer,
    StudioSerializer,
    StudioImageSerializer,
    StudioVideoSerializer
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
            data = {"token": jwt_encode_handler(jwt_payload_handler(user)), 'id': user.id}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class StudioImageListCreateView(ListCreateAPIView):
    queryset = StudioImage.objects.all()
    serializer_class = StudioImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class StudioImageRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = StudioImage.objects.all()
    serializer_class = StudioImageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
