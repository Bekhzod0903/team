from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Post, Category
from django.urls import reverse_lazy
from .forms import PostForm, BlogForm, AddReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Review 
from django.contrib import messages
from django.core.paginator import Paginator, Page


class CategoryListView(View):
    def get(self, request):
        return render(request, 'blogs/blog_list.html')

class BlogListView(View):
    template_name = 'blogs/blog_list.html'
    paginate_by = 4

    def get(self, request):
        category_id = request.GET.get('category')
        if category_id:
            posts = Post.objects.filter(category_id=category_id)
        else:
            posts = Post.objects.all()

        paginator = Paginator(posts, self.paginate_by)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        categories = Category.objects.all()
        user = request.user
        context = {'page_obj': page_obj, 'categories': categories, 'user': user}
        return render(request, self.template_name, context)

class BlogDetailView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        reviews = Review.objects.filter(post=post)
        context = {
            'post': post,
            'reviews': reviews,
            'current_user': request.user,
        }
        return render(request, 'blogs/blog_detail.html', context)

class BlogCreateView(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'blogs/add_blog.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog-list')
        return render(request, 'blogs/add_blog.html', {'form': form})

class BlogUpdateView(View):
    def get(self, request, pk):
        blog = get_object_or_404(Post, pk=pk)
        form = BlogForm(instance=blog)
        return render(request, 'blogs/update_blog.html', {'form': form, 'blog': blog})

    def post(self, request, pk):
        blog = get_object_or_404(Post, pk=pk)
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog-detail', pk=blog.pk)
        return render(request, 'blogs/update_blog.html', {'form': form, 'blog': blog})


class BlogDeleteView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blogs/delete_blog.html', {'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('blogs:blog-list')
    
class AddReviewView(LoginRequiredMixin, View):
    model = Post
    def get(self, request, pk):
        self.object = get_object_or_404(self.model, pk=pk)
        add_review_form = AddReviewForm()
        context = {
            'post': self.object,
            'add_review_form': add_review_form
        }
        return render(request, 'post/post_detail.html', context=context)

    def post(self, request, pk):
        self.object = get_object_or_404(self.model, pk=pk)
        add_review_form = AddReviewForm(request.POST)
        if add_review_form.is_valid():
            review = add_review_form.save(commit=False)
            review.post = self.object
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully.')
            return redirect('blogs:blog-detail', pk=pk)
        else:
            messages.error(request, 'Error adding review. Please check the form.')
            context = {
                'post': self.object,
                'add_review_form': add_review_form
            }
            return render(request, 'blogs/blog_detail.html', context=context)
    
class UpdateReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(instance=review)
        return render(request, 'review/update_review.html', {'form': form, 'review': review})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        form = AddReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect('blogs:blog-detail', pk=review.post_id)
        else:
            messages.error(request, 'Error updating review. Please check the form.')
        return render(request, 'review/update_review.html', {'form': form, 'review': review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        is_user = review.user == request.user
        return render(request, 'review/delete_review.html', {'review': review, 'is_user': is_user})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user:
            messages.error(request, "You are not authorized to delete this review.")
            return redirect('blogs:blog-detail', pk=review.post.pk)
        
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('blogs:blog-detail', pk=review.post.pk)