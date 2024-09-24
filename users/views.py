from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return HttpResponse("<h1>about</h1>")

def quota_request(request):
    return HttpResponse("<h1>Quota Page WIP</h1>")

def quota_result(request):
    return HttpResponse("<h1>Result Page WIP</h1>")