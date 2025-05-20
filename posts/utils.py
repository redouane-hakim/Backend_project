def xor_like(post, user, value):
    from .models import Like
    try:
        existing_like = Like.objects.get(post=post, user=user)
        if existing_like.value == value:
            # Same like exists, remove it
            existing_like.delete()
            return 'removed'
        else:
            # Toggle like value
            existing_like.value = value
            existing_like.save()
            return 'updated'
    except Like.DoesNotExist:
        Like.objects.create(post=post, user=user, value=value)
        return 'created'
