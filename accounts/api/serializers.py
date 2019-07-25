from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model, authenticate
from accounts.models import Profile, Studio,  Event

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

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
        instance.last_login = validated_data.get('last_login', instance.last_login)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_buser = validated_data.get('is_buser', instance.is_buser)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance


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


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {'is_premimum': {'read_only': True}}


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class StudioSerializer(ModelSerializer):
    class Meta:
        model = Studio
        fields = '__all__'


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'is_premimum')
        extra_kwargs = {'id': {'read_only': True}}
