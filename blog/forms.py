from django import forms
from .models import Post, Review


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'star_given']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'category']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'category']