from django.contrib import admin
from .models import Post, Product, Comment, Like, Report

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'speciality', 'created_at')
    search_fields = ('author__username', 'speciality', 'content')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'price', 'created_at')
    search_fields = ('author__username', 'speciality', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'created_at')
    search_fields = ('author__username', 'post__content')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'value')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'reporter', 'reported_user', 'status', 'created_at')
    list_filter = ('status',)
