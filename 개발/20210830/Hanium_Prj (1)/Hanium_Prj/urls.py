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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from TaskManager import views

urlpatterns = [
    path('admin/', admin.site.urls),                                        # 관리자 페이지 url 연결
    path('', views.index, name='index'),                                    # 첫 페이지

    path('login/', views.login, name='login'),                              # 로그인 url 연결
    path('logout/', views.logout, name='logout'),                           # 로그아웃 url 연결
    path('signup/', views.signup, name='signup'),                           # 회원 가입 url 연결

    path("main/", views.main, name="main"),                                 # main화면 url 연결
    path("about/", views.about, name="about"),                              # About화면 url 연결
    path("mypage/", views.MyPage, name="mypage"),                           # 마이페이지 url 연결

    # 통합기능 페이지 url 연결
    path("TaskManager/", views.Task_Manager, name="TaskManager"),
    path('TaskManager/createTodo/', views.TaskManager_createTodo, name='createTodo'),   # 투두리스트 추가
    path('TaskManager/deleteTodo/', views.TaskManager_deleteTodo, name='deleteTodo'),   # 투두리스트 삭제
    path('TaskManager/completeTodo/', views.TaskManager_completeTodo, name='completeTodo'),

    # 졸음 감지 페이지 url 연결
    path("Drowsiness/", views.Drowsiness, name="Drowsiness"),
    path('Drowsiness/createTodo/', views.Drowsiness_createTodo, name='createTodo'),
    path('Drowsiness/deleteTodo/', views.Drowsiness_deleteTodo, name='deleteTodo'),
    path('Drowsiness/completeTodo/', views.Drowsiness_completeTodo, name='completeTodo'),
    # 눈깜빡임 감지 페이지 url 연결
    path("Blinking/", views.Blinking, name="Blinking"),                     # 눈깜빡임 url 연결
    path('Blinking/createTodo/', views.Blinking_createTodo, name='createTodo'),
    path('Blinking/deleteTodo/', views.Blinking_deleteTodo, name='deleteTodo'),
    path('Blinking/completeTodo/', views.Blinking_completeTodo, name='completeTodo'),

    # 졸음 해소 스트레칭 페이지 url 연결
    path("tip/", views.tip, name="tip"),

    # 게시판 페이지 url 연결
    path("Board/", views.Board, name="Board"),
    # 자유게시판 url 연결
    path('freeboard/', views.freeboard, name='freeboard'),
    path('freeboard_writing/', views.freeboard_writing, name='freeboard_writing'),
    path('freeboard_post/<int:pk>', views.freeboard_post, name='freeboard_post'),
    path('freeboard_edit/<int:pk>', views.freeboard_edit, name='freeboard_edit'),
    path('freeboard_delete/<int:pk>', views.freeboard_delete, name='freeboard_delete'),
    path('freeboard_comment/<int:pk>', views.freeboard_comment, name='freeboard_comment'),

    # Q & A url 연결
    path('questionboard/', views.questionboard, name='questionboard'),
    path('questionboard_writing/', views.questionboard_writing, name='questionboard_writing'),
    path('questionboard_post/<int:pk>', views.questionboard_post, name='questionboard_post'),
    path('questionboard_edit/<int:pk>', views.questionboard_edit, name='questionboard_edit'),
    path('questionboard_delete/<int:pk>', views.questionboard_delete, name='questionboard_delete'),
    path('questionboard_comment/<int:pk>', views.questionboard_comment, name='questionboard_comment'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
