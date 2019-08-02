from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile, Studio, Event, Premium, PremiumBooking

User = get_user_model()


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'last_login', 'is_active',
                  'is_buser', 'is_staff', 'is_admin', 'profile', 'studio', 'premiumbook')
        extra_kwargs = {'password': {'write_only': True}}
        depth = 1

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('last_login', 'is_active', 'is_buser', 'is_staff')

    def update(self, instance, validated_data):
        instance.last_login = validated_data.get(
            'last_login', instance.last_login)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.is_buser = validated_data.get('is_buser', instance.is_buser)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    repeat_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate_repeat_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['new_password'] != data['repeat_password']:
            raise serializers.ValidationError("finish must occur after start")
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated"
                    raise serializers.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials"
                raise serializers.ValidationError(msg)
        else:
            msg = "Must provide username and password both"
            raise serializers.ValidationError(msg)
        return data


class PremiumSerializer(ModelSerializer):
    class Meta:
        model = Premium
        fields = '__all__'


class PremiumBookingSerializer(ModelSerializer):
    is_premium = serializers.SerializerMethodField()

    class Meta:
        model = PremiumBooking
        fields = ('id', 'user', 'premium', 'date_of_booking',
                  'user_premium', 'is_premium')

    def get_is_premium(self, obj):
        return obj.is_premium


class StudioSerializer(ModelSerializer):
    class Meta:
        model = Studio
        fields = '__all__'


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'is_premimum': {'read_only': True}}
        # depth = 1


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
