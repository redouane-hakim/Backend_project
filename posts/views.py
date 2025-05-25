from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Product, Comment, Like
from .serializers import PostSerializer, ProductSerializer, CommentSerializer, LikeSerializer
from .utils import xor_like

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['speciality']
    search_fields = ['content', 'speciality']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['speciality']
    search_fields = ['content', 'speciality']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check if we need to turn a Post into a Product
        if instance.price is None and 'price' in request.data:
            # If price is provided, create Product (which is a subclass of Post)
            data = request.data.copy()
            data['price'] = float(data['price'])  # Ensure price is a number
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # If price is None or being removed, treat as a Post
        if instance.price is not None and 'price' in request.data and request.data['price'] is None:
            data = request.data.copy()
            data['price'] = None
            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        type_filter = self.request.query_params.get('type')

        if type_filter == 'product':
            queryset = queryset.filter(price__isnull=False)
        elif type_filter == 'post':
            queryset = queryset.filter(price__isnull=True)

        return queryset

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)

class LikeToggleView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        value = int(request.data.get('value'))
        if value not in [1, -1]:
            return Response({"detail": "Invalid like value."}, status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.get(id=post_id)
        result = xor_like(post, request.user, value)
        return Response({"detail": f"Like {result}."})
