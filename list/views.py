from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from list.forms import LoginForm, RegistrationForm, TodoForm
from list.models import Todo


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=request.POST["username"], password=request.POST["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/index")
        else:
            return render(request, "login.html", {"form": form})
    else:
        return render(request, "login.html", {"form": LoginForm()})

    # return redirect("/index")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=request.POST["username"],
                email=request.POST["email"],
                password=request.POST["password"],
            )
            return redirect("/")
        else:
            return render(request, "register.html", {"form": form})
    else:
        return render(request, "register.html", {"form": RegistrationForm()})


def logout_view(request):
    logout(request)
    return redirect("/")


def index(request):

    item_list = Todo.objects.order_by("-date")
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()

    form = TodoForm()

    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }
    return render(request, 'base.html', page)
def editindex(request,id):
    dataedit = Todo.objects.get(id = id)
    item_list = Todo.objects.order_by("-date")

    if request.method == "POST":
        form = TodoForm(request.POST, instance = dataedit)
        if form.is_valid():
            form.save()
            return redirect('/index')
    form = TodoForm(instance = dataedit)
    page = {
        "forms": form,
        "list": item_list,
        "title": "TODO LIST",
    }

    return render(request, 'editform.html', page)


### function to remove item, it receive todo item_id as primary key from url ##
def remove(request, item_id):
    item = Todo.objects.get(id=item_id)
    item.delete()
    messages.info(request, "item removed !!!")
    return redirect('/index')
