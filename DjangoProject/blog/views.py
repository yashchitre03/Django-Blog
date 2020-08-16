from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

# Create your views here.

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


    def get_queryset(self):
        result = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            result = Post.objects.filter(title__icontains=query).order_by('-date_posted')
        return result

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if not query:
            query = ''
        context['query'] = query
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        result = Post.objects.filter(author=user)
        query = self.request.GET.get('search')
        if query:
            result = Post.objects.filter(title__icontains=query)
        return result.order_by('-date_posted')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        if not query:
            query = ''
        context['query'] = query
        return context


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'custom'})