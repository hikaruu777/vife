from django.urls import path

from .views import (
    IndexView,
    PostDetailView,
    CategoryListView,
    CategoryPostView,
    SearchView,
    SearchPostView,
)


app_name = 'posts'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<uuid:pk>', PostDetailView.as_view(), name='post_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<str:category_slug>/', CategoryPostView.as_view(), name='category_post'),
    path('search/', SearchView.as_view(), name='search'),
    path('search_post/', SearchPostView.as_view(), name='search_post'),
]