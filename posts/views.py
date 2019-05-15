from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import BrowsableAPIRenderer, HTMLFormRenderer, JSONRenderer

from posts.serializers import PostCreateSerializer
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home_view(request):
    auth_form = LoginForm()
    signup_form = SignupForm()
    return render(request, "home.html", {"auth_form": auth_form, "signup_form": signup_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                print("No userr... sad!")
        else:
            print("Invalid form bro...!", request.POST)
        return render(request, "login.html", {"form": form, "errors": "Invalid username/Password"})

    elif request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})


def user_create(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, "signup.html", {"form": form})

    elif request.method == "GET":
        form = SignupForm()
        return render(request, "signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('/')


def post_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            print(request.user.id)
            posts = Post.objects.filter(user=request.user.id)
            print(posts)
            return render(request, 'posts.html', {"posts": posts})
        else:
            return redirect('/login')


@csrf_exempt
def post_for_user(request, user):
    if request.method == "POST":
        print(request.POST, user)
        return HttpResponse("Success")


class PostCreate(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer]
    lookup_url_kwarg = "user"

    def perform_create(self, serializer):
        username = self.kwargs.get(self.lookup_url_kwarg)
        user = get_object_or_404(User, username=username)
        if user is not None:
            serializer.save(user=user)
        else:
            raise Http404
