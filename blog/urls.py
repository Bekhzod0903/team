from django.urls import path
from .views import (BlogListView, BlogDetailView, BlogCreateView,
                     BlogUpdateView, BlogDeleteView,
                     AddReviewView, UpdateReviewView, DeleteReviewView)

app_name = 'blogs'

urlpatterns = [
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog-delete'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog-update'),
    path('post/create/', BlogCreateView.as_view(), name='blog-create'),
    path('', BlogListView.as_view(), name='blog-list'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('add-review/<int:pk>/', AddReviewView.as_view(), name='add-review'),
    path('update-review/<int:pk>/', UpdateReviewView.as_view(), name='update-review'),
    path('delete-review/<int:pk>/', DeleteReviewView.as_view(), name='delete-review'),
]
