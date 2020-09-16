import os
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage

from django.views import View
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView,
                                  FormView)
from django.views.generic.detail import SingleObjectMixin

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment, Like
from .forms import CommentForm, ReportForm

# Created the views here.


def getResult(option, query):
    """Returns list of Post objects according to the option selected by user in the search bar.

    Args:
        option (str): Option from the drop-down menu.
        query (str): Search term entered.

    Returns:
        list of Post objects: The posts that matched the query.
    """

    if option == 'title':
        result = Post.objects.filter(title__icontains=query)
    elif option == 'content':
        result = Post.objects.filter(content__icontains=query)
    else:
        tags = query.split()
        result = Post.objects.filter(tags__name__in=tags)

    return result


class PostListView(ListView):
    """
    List View to display all Posts.
    """

    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_queryset(self):
        """
        Updates results by the users search terms.
        """
        result = super().get_queryset()
        option = self.request.GET.get('options')
        query = self.request.GET.get('search')

        if query:
            result = getResult(option, query)

        return result.order_by('-date_posted')

    def get_context_data(self, **kwargs):
        """
        Adds query data so that the drop-down menu does not reset.
        """
        context = super().get_context_data(**kwargs)
        option = self.request.GET.get('options')
        query = self.request.GET.get('search')

        if not query:
            query = ''

        context['option'] = option
        context['query'] = query
        return context


class UserPostListView(ListView):
    """
    Same as PostListView, but for an individual user.
    """

    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 6

    def get_queryset(self):
        """
        Updates results by the user search terms.
        """
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
        """
        Adds query data so that the drop-down menu does not reset.
        """
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
    """
    Individual post view when a GET request is received.
    """

    model = Post

    def get(self, request, *args, **kwargs):
        """
        Increments the post views if a new session is detected.
        """
        if not self.request.session.get('visited', False):
            post = Post.objects.get(pk=self.kwargs.get('pk'))
            post.view_count += 1
            post.save()

        self.request.session['visited'] = True
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Checks if user has already liked the post or not.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        post = Post.objects.get(pk=self.kwargs.get('pk'))

        if not self.request.user.is_anonymous:
            context['liked'] = post.post_likes.filter(
                user=self.request.user) and True or False

        context['title'] = post.title
        return context


class PostComment(LoginRequiredMixin, SingleObjectMixin, FormView):
    """
    Individual post view when a POST request is received.
    """

    template_name = 'blog/post_detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        """
        Logic to register user like or comment on a post.
        """
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
        """
        Adds author to the comment, and saves it.
        """
        comment = form.save(commit=False)
        comment.post = Post.objects.get(id=self.kwargs.get('pk'))
        comment.author = get_user_model().objects.get(username=self.request.user)
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns the path the user came from.
        """
        return self.request.path


class PostDetailView(View):
    """
    Passes the request to an appropriate view.
    View is for an individual post.
    """

    def get(self, request, *args, **kwargs):
        """
        Redirects to the PostContent view when a GET request is received.
        """
        view = PostContent.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Redirects to the PostComment view when a POST request is received.
        """
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new user post.
    """

    model = Post
    fields = ['title', 'content', 'tags', ]

    def form_valid(self, form):
        """
        Adds current user as author of the post.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adds title as the current post requested.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Post'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating/editing a current user post.
    """

    model = Post
    fields = ['title', 'content', 'tags', ]

    def form_valid(self, form):
        """
        Keeps current user as author of the post.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Tests whether current user is the original author of the post.
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        """
        Adds title as current post requested.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a user post.
    """

    model = Post
    success_url = '/'

    def test_func(self):
        """
        Tests whether current user is the original author of the post.
        """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        """
        Adds title as current post requested.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context


def about(request):
    """Returns the view for the about page.

    Args:
        request (object): Information about the user request.

    Returns:
        Rendered view of the 'about' template with given request and additional context.
    """
    return render(request, 'blog/about.html', {'title': 'About'})


def report(request):
    """Returns the view for the report page. If a POST request is made, the form is cleaned and sent as an email.

    Args:
        request (object): Information about the user request.

    Returns:
        Rendered view of the 'report' template with given request and additional context.
    """
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
