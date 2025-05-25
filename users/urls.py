from django.urls import path
from .views import RegisterView, ProfileView, SubscriptionView, CurrentUserView, UserProfileByIdView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('profile/<int:user_id>/', UserProfileByIdView.as_view(), name='user-profile')
]
