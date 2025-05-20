from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class BugReport(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bug_reports')
    description = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

class UserReport(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_against')
    description = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
