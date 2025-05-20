from django.urls import path
from .views import (
    PostListCreateView, ProductListCreateView, PostDetailView,
    CommentCreateView, LikeToggleView
)

app_name = 'posts'

urlpatterns = [
    path('', PostListCreateView.as_view(), name='posts-list'),
    path('products/', ProductListCreateView.as_view(), name='products-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/comment/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:post_id>/like/', LikeToggleView.as_view(), name='like-toggle'),
]
