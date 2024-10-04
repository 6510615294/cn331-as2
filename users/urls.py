from django.urls import path
from . import views

urlpatterns = [
    path('',views.login),
    path('about', views.about),
    path('request',views.quota_request),
    path('result', views.quota_result),
    path('register',views.registeration),
]