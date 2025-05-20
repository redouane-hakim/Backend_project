from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Subscription

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'trust_score')

class ProfileSerializer(serializers.ModelSerializer):
    profile_complete = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('image', 'location', 'speciality', 'phone_number', 'profile_complete')

    def get_profile_complete(self, obj):
        return obj.is_complete()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user)
        return user

class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = serializers.ReadOnlyField(source='subscriber.username')
    subscribed_to = serializers.ReadOnlyField(source='subscribed_to.username')

    class Meta:
        model = Subscription
        fields = ('id', 'subscriber', 'subscribed_to', 'created_at')
