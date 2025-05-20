from rest_framework import serializers
from .models import BugReport, UserReport
from users.serializers import UserSerializer

class BugReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = BugReport
        fields = '__all__'
        read_only_fields = ['reporter', 'status', 'created_at']

class UserReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)
    reported_user = UserSerializer(read_only=True)

    class Meta:
        model = UserReport
        fields = '__all__'
        read_only_fields = ['reporter', 'status', 'created_at']
