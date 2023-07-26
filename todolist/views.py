from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import *
from .utils import *


class ToDoListHome(DataMixin, ListView):
    model = toDoList
    template_name = "todolist/index.html"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main page")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return toDoList.objects.filter(is_published=True).select_related("cat")


"""def index(request):
    post = toDoList.objects.all()

    context = {'post': post,
               'menu': menu,
               'title': "Main page",
               'cat_selected': 0,
               }

    return render(request, 'todolist/index.html', context=context)"""


class AddSnippet(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "todolist/addpage.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add snippet")
        return dict(list(context.items()) + list(c_def.items()))


"""def add_snippet(request):
    if request.method == 'POST':
        forms = AddPostForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('home')
    else:
        forms = AddPostForm()
    return render(request, 'todolist/addpage.html', {'form': forms, 'menu': menu, 'title': 'Add Snippet'})"""


class FeedBack(DataMixin, FormView):
    form_class = ContactForm
    template_name = "todolist/feedback.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Feedback", is_home_page=True)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect("home")


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "todolist/register.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("home")


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = "todolist/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Login")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy("home")


# def login(request):
#     return HttpResponse("Login")
def logout_user(request):
    logout(request)
    return redirect("login")


def about(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.pop(0)
    return render(
        request,
        "todolist/about.html",
        {"menu": user_menu, "title": "About this site", "is_home_page": True},
    )


class ShowPost(DataMixin, DetailView):
    model = toDoList
    template_name = "todolist/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="post")
        return dict(list(context.items()) + list(c_def.items()))


"""def show_post(request, post_slug):
    post = get_object_or_404(toDoList, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'tittle': post.title,
        'cat_selected': post.cat_id,
    }

    return render(request, 'todolist/post.html', context=context)"""


class ToDoListCategory(DataMixin, ListView):
    model = toDoList
    template_name = "todolist/index.html"
    context_object_name = "post"
    allow_empty = False

    def get_queryset(self):
        return toDoList.objects.filter(cat__slug=self.kwargs["cat_slug"], is_published=True).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs["cat_slug"])
        c_def = self.get_user_context(title="Category - " + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


"""def show_category(request, cat_slug):
    post = toDoList.objects.filter(cat__slug=cat_slug)

    context = {'post': post,
               'title': "Section display",
               'cat_selected': cat_slug,
               }

    return render(request, 'todolist/index.html', context=context)"""


def pageNotFound(request, exception):
    return HttpResponseNotFound(f"<h1>This page doesn't exists</h1>")
