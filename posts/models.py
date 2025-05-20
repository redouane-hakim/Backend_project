from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    speciality = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='post_images/', null=True, blank=True)

    def __str__(self):
        return f"Post by {self.author.username}"

class Product(Post):
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    LIKE_CHOICES = (
        (1, 'Thumbs Up'),
        (-1, 'Thumbs Down'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=LIKE_CHOICES)

    class Meta:
        unique_together = ('post', 'user')  # XOR enforced via logic

class Report(models.Model):
    REPORT_CHOICES = (
        ('post', 'Post'),
        ('user', 'User'),
    )
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    reported_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='reports_received')
    report_type = models.CharField(max_length=10, choices=REPORT_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
