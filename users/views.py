from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Subject, Student
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    return render(request, "login.html")

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
            User_Pass = User.objects.create(
                username = Student_ID,
                password = password
            )
            User_Pass.save()
             
            Naksuksa =Student.objects.create(
                SID = Student_ID,
                first = name,
                last = surname,
            )
            
            # User_Pass = User
            #     SID =Student_ID,
            #     username = username,
            #     password = password,
            #     password2 = password2,
            Naksuksa.save()
            messages.success(request, "registered successfully")
            return redirect("/")
    else:
        return render(request, "register.html")