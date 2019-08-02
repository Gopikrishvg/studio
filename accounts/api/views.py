import jwt
from datetime import time
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib.auth import get_user_model, login, logout
from django.core import signing
from django.core.mail import send_mail
from django.utils import timezone
from accounts.models import (
    Profile,
    Event,
    Studio,
    PasswordReset,
    Premium,
    PremiumBooking,
)
from .serializers import (
    UserSerializer,
    UserUpdateSerializer,
    UserLoginSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    ProfileSerializer,
    EventSerializer,
    StudioSerializer,
    PremiumSerializer,
    PremiumBookingSerializer,
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
                'is_staff': user.is_staff,
                'is_admin': user.is_admin,
                "token": jwt_encode_handler(jwt_payload_handler(user)),
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangeView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PasswordChangeSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)

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


class OtpTokenView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        d = User.objects.filter(email__iexact=email)
        print(d[0].id, d[0].email)
        value = signing.dumps({"id": d[0].id})
        send_mail(
            'OTP TOKEN - STUDIO',
            '%s Use this OTP Token to reset your password' % (value),
            "gopi@desss.com",
            [d[0].email],
            fail_silently=False,
        )
        # signing.loads(value)
        PasswordReset.objects.create(send=d[0].id, receive=0)
        data = {'token': signing.loads(value)}
        return Response(data)


class OtpValidationView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        otp = request.data.get('otp')
        data = {'token': signing.loads(otp)}
        id = data.get("token").get("id")
        obj = PasswordReset.objects.filter(send=id).order_by('-date').first()
        update_obj = PasswordReset.objects.get(id=obj.id)
        print(update_obj.receive, update_obj.date)
        if update_obj.receive == str(0):
            update_obj.receive = 1
            update_obj.save()
        else:
            return Response({"id": "0", "status": "Already password setted or resend the token"})
        t = timezone.now() - update_obj.date
        if(t.seconds < 300):
            return Response({"id": obj.send, "status": "success"})
        return Response({"id": "0", "status": "time out"})


class PasswordResetView(UpdateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PasswordResetSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        print(id)
        obj = PasswordReset.objects.filter(send=id).order_by('-date').first()
        check = PasswordReset.objects.get(id=obj.id)
        timedelta = timezone.now() - check.date
        if check.receive == str(0):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if timedelta.seconds > 360:
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)
        self.object = self.get_object()
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
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


class PremiumListCreateView(ListCreateAPIView):
    queryset = Premium.objects.all()
    serializer_class = PremiumSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PremiumRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Premium.objects.all()
    serializer_class = PremiumSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PremiumBookingListCreateView(ListCreateAPIView):
    queryset = PremiumBooking.objects.all()
    serializer_class = PremiumBookingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PremiumBookingRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = PremiumBooking.objects.all()
    serializer_class = PremiumBookingSerializer
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
