from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from .models import Post


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
