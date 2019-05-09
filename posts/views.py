from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login
from .models import Post
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def home_view(request):
    auth_form = LoginForm()
    signup_form = SignupForm()
    return render(request, "home.html", {"auth_form": auth_form, "signup_form": signup_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
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


@csrf_exempt
def post_view(request, username):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, 'posts.html', {"posts": posts})
    elif request.method == "POST":
        print(request.POST)
        return redirect('/')
