"""Hanium_Prj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from TaskManager import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),                                        # 관리자
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),   # 로그인
    path('signup/', views.signup, name='signup'),                           # 회원 가입
    path("main/", views.main, name="main"),                                 # main화면 url 연결
    path("about/", views.about, name="about"),                              # About화면 url 연결

    path("TaskManager/", views.Task_Manager, name="TaskManager"),           # 통합 기능 url 연결
    path("Drowsiness/", views.Drowsiness, name="Drowsiness"),               # 졸음감지 url 연결
    path("Blinking/", views.Blinking, name="Blinking"),                     # 눈깜빡임 url 연결

    path('task_manager', views.task_manager, name='task_manager'),          # 통합기능 url 연결
    path('sleep_detector', views.sleep_detector, name='sleep_detector'),    # 졸음감지 url 연결
    path('blink_detector', views.blink_detector, name='blink_detector'),    # 눈깜빡임 url 연결

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
