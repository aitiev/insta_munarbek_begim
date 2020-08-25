from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation', 'image', 'first_name', 'last_name']


    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email has already been used for registration')
        return email

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirmation = validated_data.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(email, password, **validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email,
                                password=password)
            print(Token.objects.filter(user=user))
            if not user:
                msg = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = "To log in 'email' and 'password' must be provided."
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs