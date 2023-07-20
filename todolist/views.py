from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *

menu = [{'title': 'Create snippet', 'url_name': 'create'},
        {'title': 'Delete snippet', 'url_name': 'delete'},
        {'title': 'About site', 'url_name': 'about'},
        {'title': 'Login', 'url_name': 'login'}]


def index(request):
    post = toDoList.objects.all()
    cats = Category.objects.all()

    context = {'post': post,
               'menu': menu,
               'cats': cats,
               'title': "Main page",
               'cat_selected': 0,
               }

    return render(request, 'todolist/index.html', context=context)

def add_snippet(request):
    return HttpResponse("Add snippet")

def delete_snippet(request):
    return HttpResponse("Delete snippet")

def login(request):
    return HttpResponse("Login")
def about(request):
    return render(request, 'todolist/about.html', {'title': 'About this site', 'desc': 'Site description'})

def show_post(request, post_id):
    return HttpResponse(f"Post with id equal {post_id}")

def show_category(request, cat_id):
    post = toDoList.objects.filter(cat_id = cat_id)
    cats = Category.objects.all()

    if len(post) ==0:
        raise Http404()

    context = {'post': post,
               'menu': menu,
               'cats': cats,
               'title': "Section display",
               'cat_selected': cat_id,
               }

    return render(request, 'todolist/index.html', context=context)
def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>This page doesn't exists</h1>")
