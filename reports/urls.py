from django.urls import path
from .views import BugReportCreateView, UserReportCreateView

app_name = 'reports'

urlpatterns = [
    path('bugs/', BugReportCreateView.as_view(), name='bug-report'),
    path('users/', UserReportCreateView.as_view(), name='user-report'),
]
