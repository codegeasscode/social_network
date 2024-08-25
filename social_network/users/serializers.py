from rest_framework import serializers
from .models import CustomUser, FriendRequest
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'username', 'first_name', 'last_name')

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        # Create a new user instance
        user = CustomUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # Set the password
        user.set_password(password)

        # Save the user to the database
        user.save()

        return user
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']
