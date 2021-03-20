from django.db.models import Count, Q

from posts.models import Category


def common(request):
    context = {
        'categories': Category.objects.annotate(
            num_posts=Count('post', filter=Q(post__is_public=True))),
    }
    return context
