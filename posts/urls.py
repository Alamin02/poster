from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('login/', views.user_login, name="login"),
    path('signup/', views.user_create, name="signup"),
    path('posts/<str:username>', views.post_view, name="posts"),
]
