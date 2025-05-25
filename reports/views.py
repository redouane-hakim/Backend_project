from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post
from .models import BugReport, UserReport, PostReport
from .serializers import BugReportSerializer, UserReportSerializer, PostReportSerializer
from rest_framework import serializers


class BugReportCreateView(generics.CreateAPIView):
    serializer_class = BugReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

class UserReportCreateView(generics.CreateAPIView):
    serializer_class = UserReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        reported_user_id = self.request.data.get("reported_user")

        if not reported_user_id:
            raise serializers.ValidationError({"reported_user": "Missing reported_user ID."})

        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            reported_user = User.objects.get(id=reported_user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"reported_user": "User not found."})

        serializer.save(reporter=self.request.user, reported_user=reported_user)




class PostReportCreateView(generics.CreateAPIView):
    serializer_class = PostReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id")
        description = request.data.get("description", "")

        if not post_id:
            return Response({"detail": "post_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if post.author == request.user:
            return Response({"detail": "You cannot report your own post."}, status=status.HTTP_403_FORBIDDEN)

        # Create the report
        report = PostReport.objects.create(
            reporter=request.user,
            post=post,
            report_type="post",
            description=description
        )

        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MyAllReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        post_reports = PostReport.objects.filter(reporter=user)
        user_reports = UserReport.objects.filter(reporter=user)
        bug_reports = BugReport.objects.filter(reporter=user)

        return Response({
            "post_reports": PostReportSerializer(post_reports, many=True).data,
            "user_reports": UserReportSerializer(user_reports, many=True).data,
            "bug_reports": BugReportSerializer(bug_reports, many=True).data
        })
