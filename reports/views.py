from rest_framework import generics, permissions
from .models import BugReport, UserReport
from .serializers import BugReportSerializer, UserReportSerializer

class BugReportCreateView(generics.CreateAPIView):
    serializer_class = BugReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

class UserReportCreateView(generics.CreateAPIView):
    serializer_class = UserReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
