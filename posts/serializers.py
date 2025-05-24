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
    image = serializers.ImageField(required=False, allow_null=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)# <-- add this line

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'speciality', 'contact_info','price', 'image', 'created_at', 'comments', 'likes_count']

    def create(self, validated_data):
        if 'price' in validated_data:
            # If it's a product, make sure price is added
            return Product.objects.create(**validated_data)  # Assuming Product is a subclass of Post
        else:
            return Post.objects.create(**validated_data)  # Normal post without price

    def get_likes_count(self, obj):
        return obj.likes.filter(value=1).count() - obj.likes.filter(value=-1).count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add a special field to check if the post is actually a Product
        if isinstance(instance, Product):
            representation['is_product'] = True
        else:
            representation['is_product'] = False
        return representation

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
