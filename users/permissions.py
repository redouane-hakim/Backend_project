from rest_framework import permissions

class IsProfileComplete(permissions.BasePermission):
    """
    Allows access only if user profile is complete.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, 'profile', None)
        if profile is None:
            return False
        return profile.is_complete()
