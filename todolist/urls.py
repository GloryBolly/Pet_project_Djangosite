from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path("", ToDoListHome.as_view(), name="home"),
    path("about/", about, name="about"),
    path("create/", AddSnippet.as_view(), name="create"),
    path("feedback/", FeedBack.as_view(), name="feedback"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("post/<slug:post_slug>/", ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", ToDoListCategory.as_view(), name="category"),
]
