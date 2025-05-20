from django_filters import rest_framework as filters
from .models import Post

class PostFilter(filters.FilterSet):
    speciality = filters.CharFilter(field_name='speciality', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ['speciality']
