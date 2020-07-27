from django.shortcuts import render
from django.http import HttpResponse


posts = [
    {
        'author': 'Yash',
        'title': 'My first post',
        'content': 'Hello, world!',
        'date_posted': '26 July, 2020',
    },
    {
        'author': 'Corey',
        'title': 'last post',
        'content': 'Bye, bye world!',
        'date_posted': '28 August, 2018',
    }
]


# Create your views here.
def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'custom'})