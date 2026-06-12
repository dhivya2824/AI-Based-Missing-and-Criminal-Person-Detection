"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from .views import home,index, RegisterView,logout_view
from .import views

urlpatterns = [
    path('', home, name='users-home'),
    path('profile/', views.home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile1/', views.profile, name='users-profile'),
    path('chatbot/', views.chatbot_response_view,name='chatbot'),
    path('logout_view/',logout_view,name='logout_view'),
    path('admin-register/', views.admin_register, name='admin-register'),
    path('admin-login/', views.admin_login, name='admin-login'),
    path('admin-logout/', views.admin_logout, name='admin-logout'),






    path('register-case/', views.register_case, name='register_case'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('detect/', views.detect_person, name='detect-person'),
    path('start_Detection/', views.start_Detection, name='start_Detection'),
    path('video-detection/', views.detect_from_video, name='video-detection'),
    path('delete/<int:case_id>/', views.delete_case, name='delete_case'),   
    





]
