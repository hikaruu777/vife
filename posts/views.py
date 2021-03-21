from django.db.models import Count, Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from posts.models import Post, Category


class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if not post.is_public and not self.request.user.is_authenticated:
            raise Http404
        return post


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.order_by('-created_at')[:10]


class CategoryListView(ListView):
    queryset = Category.objects.annotate(
        num_posts=Count('post', filter=Q(post__is_public=True))
    )


class CategoryPostView(ListView):
    model = Post
    template_name = 'posts/category_post.html'

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        self.category = get_object_or_404(Category, slug=category_slug)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class SearchView(TemplateView):
    template_name = 'posts/search.html'


class SearchPostView(ListView):
    model = Post
    template_name = 'posts/search_post.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', None)
        lookups = (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )
        if query is not None:
            qs = super().get_queryset().filter(lookups).distinct()
            return qs
        qs = super().get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context
