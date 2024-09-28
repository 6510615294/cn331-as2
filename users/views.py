from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    name = "Kawin"
    surname = "Sangsivarit"
    return render(request, "index.html", {"name":name, "surname":surname})

def about(request):
    return render(request, "about.html")

def quota_request(request):
    return render(request, "quota_request.html")

def quota_result(request):
    return render(request, "quota_result.html")