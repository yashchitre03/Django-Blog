from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your views here.
def getResult(option, query):
    if option == 'title':
        result = Post.objects.filter(title__icontains=query)
    elif option == 'content':
        result = Post.objects.filter(content__icontains=query)
    else:
        tags = query.split()
        result = Post.objects.filter(tags__name__in=tags)
    return result

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


    def get_queryset(self):
        result = super().get_queryset()
        option = self.request.GET.get('options')
        query = self.request.GET.get('search')
        if query: result = getResult(option, query)
        return result.order_by('-date_posted')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        option = self.request.GET.get('options')
        query = self.request.GET.get('search')
        if not query:
            query = ''
        context['option'] = option
        context['query'] = query
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6


    def get_queryset(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        option = self.request.GET.get('options')
        query = self.request.GET.get('search')
        result = Post.objects
        if query: result = getResult(option, query)
        result = result.filter(author=user)
        return result.order_by('-date_posted')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        option = self.request.GET.get('options')
        query = self.request.GET.get('search')
        if not query:
            query = ''
        context['option'] = option
        context['query'] = query
        return context

class PostDetailView(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        post.view_count += 1
        post.save()
        return super().get(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        comments = Comment.objects.filter(post=post)
        context['comments'] = comments
        return context


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