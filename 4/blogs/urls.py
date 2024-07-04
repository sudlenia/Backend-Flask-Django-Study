from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BlogListView,
    BlogDetailView,
    BlogCreateView,
    BlogUpdateView,
    BlogDeleteView,
)

urlpatterns = [
    path("new/", BlogCreateView.as_view(), name="post_new"),
    # path("<int:pk>/", BlogDetailView.as_view(), name="post_detail"),
    path("<slug:slug>/", BlogDetailView.as_view(), name="post_detail"),
    path("<slug:slug>/edit/", BlogUpdateView.as_view(), name="post_edit"),
    path("<slug:slug>/delete/", BlogDeleteView.as_view(), name="post_delete"),
    path("", BlogListView.as_view(), name="post_list"),
]
