from rest_framework import serializers

from .models import CustomUser
from django.contrib.auth import authenticate


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'role')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ShortUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    
    def get_profile_image(self, obj):
        from apps.maintenance.serializers import ImageSerializer
        return ImageSerializer(obj.profile_image).data


    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'role', 'profile_image')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)
    username = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email/password combination.')
        
        # Add the user object to attrs, so we can use it later in the view
        attrs['user'] = user
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()