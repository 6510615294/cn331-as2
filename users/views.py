from django.shortcuts import render,redirect
from .models import Subject, Student
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

# Create your views here.
@csrf_exempt
def login_toweb(request):
    if request.user.is_authenticated :
        user = request.user
        
        return render(request, "quota_request.html")
        
    elif request.method == "POST" :
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        print(user)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect("/admin")
            return render(request, "quota_request.html")
        else:
            messages.error(request, "Invalid Username or Password")
            return render(request, "login.html")
    return render(request, "login.html")
            
def logout_formweb(request):
    logout(request)
    return redirect("/")

def about(request):
    return render(request, "about.html")

def quota_request(request):
    data=Subject.objects.all()
    return render(request, "quota_request.html",{"subjects":data})

def quota_result(request):
    return render(request, "quota_result.html")

def registeration(request):
    if request.method == "POST":
        Student_ID = request.POST["Student ID"]
        name = request.POST["name"]
        surname = request.POST["surname"]

        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password != password2:
            messages.error(request, "Password must be the same one!")
            return redirect("register")
        else:
            User_Pass = User.objects.create_user(
                username = Student_ID,
                password = password
            )
            User_Pass.save()
             
            Naksuksa =Student(SID = User_Pass,
                              first = name,
                              last = surname)
            Naksuksa.save()
            messages.success(request, "registered successfully")
            return redirect("/")
    else:
        return render(request, "register.html")