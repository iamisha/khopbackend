from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Users

extra_kwargs = {
    "password": {
        'write_only': True,
        'required': True,
        'style': {'input_type': 'password'}
    },
}

class UserSerializer(ModelSerializer):
    password = serializers.CharField(**extra_kwargs['password'],validators=[validate_password])
    class Meta:
        model=Users
        fields=["email","phone_no","password"]

    def validate_email(self, value):
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        user = Users.objects.create_user(
            phone_no=validated_data['phone_no'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(**extra_kwargs['password'])
    email=serializers.EmailField()


class UserDisplayserializer(ModelSerializer):
    class Meta:
        model=Users
        fields=["email","phone_no","date_of_birth"]
    