from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Subject, Student
from django.contrib import messages

# Create your views here.
def index(request):
    name = "Kawin"
    surname = "Sangsivarit"
    return render(request, "index.html", {"name":name, "surname":surname})

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
        faculty = request.POST["faculty"]
        
        Naksuksa =Student.objects.create(
            SID= Student_ID,
            first = name,
            last = surname,
            faculty = faculty
        )
        Naksuksa.save()
        messages.success(request, "registered successfully")
        return redirect("/")
    else:
        return render(request, "register.html")