from django.contrib import admin
from .models import BugReport, UserReport

@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'description', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'reported_user', 'description', 'status', 'created_at')
    list_filter = ('status',)
