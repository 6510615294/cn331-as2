from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_toweb),
    path('about', views.about),
    path('request',views.quota_request),
    path('result', views.quota_result),
    path('register',views.registeration),
    path('logout', views.logout_formweb),
    path('register_subject/<int:subject_id>/', views.register_subject, name='register_subject'),
]