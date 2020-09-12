from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  FormView)
# from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from .models import Post, Comment, Like
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from .forms import CommentForm, ReportForm
import os
from django.core.mail import EmailMessage
from django.contrib import messages

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
        if query:
            result = getResult(option, query)
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
        user = get_object_or_404(
            get_user_model(), username=self.kwargs.get('username'))
        option = self.request.GET.get('options')
        query = self.request.GET.get('search')
        result = Post.objects
        if query:
            result = getResult(option, query)
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
        context['title'] = self.kwargs.get('username')
        return context


class PostContent(DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        if not self.request.session.get('visited', False):
            post = Post.objects.get(pk=self.kwargs.get('pk'))
            post.view_count += 1
            post.save()
        self.request.session['visited'] = True
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()

        post = Post.objects.get(pk=self.kwargs.get('pk'))
        if not self.request.user.is_anonymous:
            context['liked'] = post.post_likes.filter(
                user=self.request.user) and True or False

        context['title'] = post.title
        return context


class PostComment(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'like':
            post = Post.objects.get(pk=self.kwargs.get('pk'))
            newLike, created = Like.objects.get_or_create(
                post=post, user=request.user)
            if not created:
                newLike.delete()

            return redirect(request.path)
        else:
            return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = Post.objects.get(id=self.kwargs.get('pk'))
        comment.author = get_user_model().objects.get(username=self.request.user)
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path


class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PostContent.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tags', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'tags', ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            mail_subject = f'Issue {form.cleaned_data["category"]}: {form.cleaned_data["subject"]}'
            mail_body = form.cleaned_data['message']
            mail_id = os.environ.get('DJANGO-E')
            mail = EmailMessage(mail_subject, mail_body,
                                from_email=mail_id, to=[mail_id])
            mail.send()

            messages.success(
                request, 'The issue has been reported to the admins')
        else:
            messages.error(request, 'Form submission failed.')
        return redirect('blog-home')
    else:
        form = ReportForm()
        context = {'form': form, 'title': 'Report'}
    return render(request, 'blog/report.html', context)
