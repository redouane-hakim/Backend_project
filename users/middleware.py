from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    """
    Redirect logged, in users to complete their profile if incomplete.
    Skip for profile update, logout, and auth endpoints.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            allowed_paths = [
                reverse('users:profile'),
                reverse('users:logout'),
                reverse('users:login'),
                reverse('users:register'),
            ]
            if not request.user.profile.is_complete() and request.path not in allowed_paths and not request.path.startswith('/admin'):
                return redirect('users:profile')
        return self.get_response(request)
