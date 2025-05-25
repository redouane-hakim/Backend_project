from django.urls import path
from .views import BugReportCreateView, UserReportCreateView, PostReportCreateView, MyAllReportsView

app_name = 'reports'

urlpatterns = [
    path('bugs/', BugReportCreateView.as_view(), name='bug-report'),
    path('users/', UserReportCreateView.as_view(), name='user-report'),

    path('posts/', PostReportCreateView.as_view(), name='report-post'),

    path('my-reports/', MyAllReportsView.as_view(), name='my-reports'),
]
