from rest_framework import serializers
from .models import Post, Product, Comment, Like, Report
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'value']
        read_only_fields = ['user']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'speciality', 'contact_info', 'created_at', 'comments', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.filter(value=1).count() - obj.likes.filter(value=-1).count()

class ProductSerializer(PostSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta(PostSerializer.Meta):
        model = Product
        fields = PostSerializer.Meta.fields + ['price']

class ReportSerializer(serializers.ModelSerializer):
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['reporter', 'status', 'created_at']
