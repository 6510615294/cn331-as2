from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_toweb),
    path('request',views.quota_request),
    path('result', views.quota_result),
    path('register',views.registration),
    path('logout', views.logout_formweb),
    path('register_subject/<int:subject_id>/', views.register_subject, name='register_subject'),
    path('cancel_registration/<int:subject_id>/', views.cancel_registration, name='cancel_registration'),
]