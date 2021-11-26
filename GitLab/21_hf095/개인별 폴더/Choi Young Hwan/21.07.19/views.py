from django.http.response import StreamingHttpResponse
from TaskManager.sleep import Sleep_Detector
from TaskManager.sleep import Blink_Detector
from TaskManager.sleep import sleep_Blink_Detector

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .models import DailyTodo
from django.views import generic

"""class Todo_List(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = './templates/Drowsiness.html'
        daily_todo = Todo_List.objects.all()
        return render(request, template_name, {"daily_todo": daily_todo})"""

# 회원 가입
def signup(request):
    global errorMsg
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']

        try:
            if not (username and password and confirm and firstname and lastname and email):
                errorMsg = '빈칸이 존재합니다!'
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=firstname,
                    last_name=lastname
                ).save()
                return redirect('/signup')
        except:
            errorMsg = '빈칸이 존재합니다!'

        return render(request, 'signup.html', {'error': errorMsg})

    return render(request, 'signup.html')

# 로그인
def login(request):
    # POST 요청시
    if request.method == 'POST':                                        # 로그인 버튼 클릭
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        try:
            if not (username and password):                             # 아이디/비밀번호 중 빈칸이 존재할 때
                errorMsg = '아이디/비밀번호를 입력하세요.'
            else:                                                       # 아이디/비밀번호 모두 입력됐을 때
                user = User.objects.get(username = username)            # 등록된 아이디의 정보 가져오기
                if check_password(password, user.password):             # 등록된 아이디의 비밀번호가 맞으면
                    request.session['user'] = user.id                   # 세션에 아이디 추가
                    request.session['email'] = user.email               # 세션에 이메일 추가
                    request.session['first_name'] = user.first_name
                    request.session['last_name'] = user.last_name
                    return redirect('/main')                                # 메인 페이지 이동
                else:                                                   # 등록된 아이디의 비밀번호가 틀리면
                    errorMsg = '비밀번호가 틀렸습니다.'
        except:                                                         # 등록된 아이디의 정보가 없을 때
            errorMsg = '가입하지 않은 아이디 입니다.'

        return render(request, 'login.html', {'error': errorMsg})   # 에러 메세지와 로그인 페이지(login.html) 리턴
    # GET 요청시
    return render(request, 'login.html')                            # 로그인 페이지(login.html) 리턴



# 로그아웃
def logout(request):
    del(request.session['user'])    # 세션에서 사용자정보 삭제
    return redirect('/')            # 로그인 페이지(login.html) 리턴

def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, '404.html', {})


# Create your views here.
def main(req):
    context = {

    }
    return render(req, "main.html", context=context)


def about(req):
    context = {

    }
    return render(req, "about.html", context=context)


def Task_Manager(req):
    context = {

    }
    return render(req, "TaskManager.html", context=context)


def Drowsiness(req):
    context = {

    }
    return render(req, "Drowsiness.html", context=context)


def Blinking(req):
    context = {

    }
    return render(req, "Blinking.html", context=context)

def Board(req):
    context = {

    }
    return render(req, "Board.html", context=context)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def task_manager(request):
    return StreamingHttpResponse(gen(sleep_Blink_Detector()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def sleep_detector(request):
    return StreamingHttpResponse(gen(Sleep_Detector()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def blink_detector(request):
    return StreamingHttpResponse(gen(Blink_Detector()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
