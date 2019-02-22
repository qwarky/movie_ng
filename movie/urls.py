from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.api_root),
    path('movies/', views.MovieListCreate.as_view(), name='movies-list'),
    path('comments/', views.CommentListCreate.as_view(), name='comments-list'),
    path('top/', views.MovieTopList.as_view(), name='movies-top-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)