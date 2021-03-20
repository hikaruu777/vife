from django.views.generic import TemplateView, ListView

from posts.models import Post


class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.order_by('-created_at')[:10]


class AboutPageView(TemplateView):
    template_name = 'about.html'