from django.shortcuts import render
from django.http import HttpResponse
from .models import Subject

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