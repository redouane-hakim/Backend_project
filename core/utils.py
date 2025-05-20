from django.db.models import Count, F, FloatField, ExpressionWrapper
from django.contrib.auth import get_user_model

User = get_user_model()

def get_recommended_users():
    # Annotate users with post_count and trust_score
    users = User.objects.annotate(
        post_count=Count('posts'),
        trust=F('trust_score')
    ).filter(trust__gt=0)  # Avoid division by zero

    # Annotate ratio = post_count / trust_score
    users = users.annotate(
        ratio=ExpressionWrapper(F('post_count') * 1.0 / F('trust'), output_field=FloatField())
    ).order_by('-ratio')

    return users
