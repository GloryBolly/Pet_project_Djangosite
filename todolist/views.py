from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm
from .models import *

menu = [
    {"title": "Create snippet", "url_name": "create"},
    {"title": "Delete snippet", "url_name": "delete"},
    {"title": "About site", "url_name": "about"},
    {"title": "Login", "url_name": "login"},
]


class ToDoListHome(ListView):
    model = toDoList
    template_name = "todolist/index.html"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        context["title"] = "Main page"
        context["cat_selected"] = 0
        return context

    def get_queryset(self):
        return toDoList.objects.filter(is_published=True)


"""def index(request):
    post = toDoList.objects.all()

    context = {'post': post,
               'menu': menu,
               'title': "Main page",
               'cat_selected': 0,
               }

    return render(request, 'todolist/index.html', context=context)"""


class AddSnippet(CreateView):
    form_class = AddPostForm
    template_name = "todolist/addpage.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        context["title"] = "Create Snippet"
        return context


"""def add_snippet(request):
    if request.method == 'POST':
        forms = AddPostForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('home')
    else:
        forms = AddPostForm()
    return render(request, 'todolist/addpage.html', {'form': forms, 'menu': menu, 'title': 'Add Snippet'})"""


def delete_snippet(request):
    return HttpResponse("Delete snippet")


def login(request):
    return HttpResponse("Login")


def about(request):
    return render(
        request,
        "todolist/about.html",
        {"title": "About this site", "desc": "Site description"},
    )


class ShowPost(DetailView):
    model = toDoList
    template_name = "todolist/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        context["title"] = context["post"]
        return context


"""def show_post(request, post_slug):
    post = get_object_or_404(toDoList, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'tittle': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'todolist/post.html', context=context)"""


class ToDoListCategory(ListView):
    model = toDoList
    template_name = "todolist/index.html"
    context_object_name = "post"
    allow_empty = False

    def get_queryset(self):
        return toDoList.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category - " + str(context["post"][0].cat)
        context["menu"] = menu
        context["cat_selected"] = context["post"][0].cat_id
        return context


"""def show_category(request, cat_slug):
    post = toDoList.objects.filter(cat__slug=cat_slug)

    context = {'post': post,
               'title': "Section display",
               'cat_selected': cat_slug,
               }

    return render(request, 'todolist/index.html', context=context)"""


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>This page doesn't exists</h1>")
