from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from core.permissions import IsAdminUser
from .serializers import (
    UserRegistrationSerializer, UserSerializer, ProfileSerializer, SubscriptionSerializer
)
from .models import Profile, Subscription

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class SubscriptionView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        subscribed_to_id = request.data.get('subscribed_to')
        if not subscribed_to_id:
            return Response({"detail": "subscribed_to is required."}, status=status.HTTP_400_BAD_REQUEST)
        if int(subscribed_to_id) == request.user.id:
            return Response({"detail": "You cannot subscribe to yourself."}, status=status.HTTP_400_BAD_REQUEST)
        subscribed_to = User.objects.filter(id=subscribed_to_id).first()
        if not subscribed_to:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        # Subscription XOR logic:
        sub, created = Subscription.objects.get_or_create(subscriber=request.user, subscribed_to=subscribed_to)
        if not created:
            sub.delete()
            # decrease trust score
            subscribed_to.trust_score -= 1
            subscribed_to.save()
            return Response({"detail": "Unsubscribed."})
        else:
            # increase trust score
            subscribed_to.trust_score += 1
            subscribed_to.save()
            return Response({"detail": "Subscribed."})
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        profile = user.profile
        profile_data = ProfileSerializer(profile).data
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'profile': profile_data,
        })
class UserListAdminView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)