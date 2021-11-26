from django.http.response import StreamingHttpResponse
from TaskManager.sleep import Sleep_Detector
from TaskManager.sleep import Blink_Detector
from TaskManager.sleep import sleep_Blink_Detector
from TaskManager.sleep import D_time
from TaskManager.models import *

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

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
            elif password != confirm:
                errorMsg = '비밀번호가 일치하지 않습니다!'
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=firstname,
                    last_name=lastname
                ).save()
                return redirect('')         # 회원가입 성공했다는 메시지 출력 후 로그인 페이지로 이동
        except:
            errorMsg = '빈칸이 존재합니다!'
        return render(request, 'signup.html', {'error': errorMsg})
    # 회원가입 성공 후 이동
    return render(request, 'signup.html')


# 로그인
def login(request):
    # POST 요청시
    if request.method == 'POST':                                        # 로그인 버튼 클릭
        username = request.POST['username']
        password = request.POST['password']
        try:
            if not (username and password):                             # 아이디/비밀번호 중 빈칸이 존재할 때
                errorMsg = '아이디/비밀번호를 입력하세요.'
            else:                                                       # 아이디/비밀번호 모두 입력됐을 때
                user = User.objects.get(username=username)              # 등록된 아이디의 정보 가져오기
                if check_password(password, user.password):             # 등록된 아이디의 비밀번호가 맞으면
                    request.session['id'] = user.id                     # 세션에 번호 추가
                    request.session['username'] = user.username         # 세션에 아이디 추가
                    request.session['email'] = user.email                   # 세션에 이메일 추가
                    request.session['first_name'] = user.first_name         # 세션에 이름 추가
                    request.session['last_name'] = user.last_name           # 세션에 성 추가
                    return redirect('main/')
                else:                                                   # 등록된 아이디의 비밀번호가 틀리면
                    errorMsg = '비밀번호가 틀렸습니다.'
        except:                                                         # 등록된 아이디의 정보가 없을 때
            errorMsg = '가입하지 않은 아이디 입니다.'

        return render(request, 'login.html', {'error': errorMsg})   # 에러 메세지와 로그인 페이지(login.html) 리턴
    # GET 요청시
    return render(request, 'login.html')                            # 로그인 페이지(login.html) 리턴


# 로그아웃
def logout(request):
    del(request.session['id'])    # 세션에서 사용자정보 삭제
    del(request.seesion['username'])
    return redirect('/')            # 메인 페이지(index.html) 리턴


def page_not_found(request, exception):
    """
    404 Page not found
    """
    return render(request, '404.html', {})


# 메인 페이지
def main(request):
    username = None
    if request.session.get('id', None):
        id = request.session.get('id', None)
        username = request.session.get('username', None)
    # html로 세션 데이터 전송
    context = {
        'id' : id,            # 사용자 번호
        'username': username  # 사용자 아이디
    }
    return render(request, "main.html", context=context)


# About 페이지
def about(request):
    context = {

    }
    return render(request, "about.html", context=context)


# 마이페이지 임시
def MyPage(request):
    id = None
    username = None

    if request.session.get('id'):
        id = AuthUser.objects.get(id=request.session.get('id', None))
        username = AuthUser.objects.get(username=request.session.get('username', None))
    context = {
        'id':id,
        'username':username,
    }
    return render(request, 'mypage.html', context=context)

ID=None
USERNAME=None
# 통합 페이지
def Task_Manager(request):
    id = None
    username = None
    if request.session.get('id'):
        id = request.session.get('id', None)
        username = request.session.get('username', None)
        global ID
        ID=id
        global USERNAME
        USERNAME=username
    context = {
        'id':id,
        'username':username
    }
    return render(request, "TaskManager.html", context=context)


# 졸음 감지 페이지
def Drowsiness(request):
    id = None
    username = None
    if request.session.get('id'):
        id = request.session.get('id', None)
        username = request.session.get('username', None)
    context = {
        'id':id,
        'username':username
    }
    return render(request, "Drowsiness.html", context=context)

# 눈 깜빡임 감지 페이지
def Blinking(request):
    id = None
    username = None
    if request.session.get('id'):
        id = request.session.get('id', None)
        username = request.session.get('username', None)
    context = {
        'id':id,
        'username':username
    }
    return render(request, "Blinking.html", context=context)


# 게시판 페이지
def Board(request):
    id = None
    username = None
    if request.session.get('id'):
        id = request.session.get('id', None)
        username = request.session.get('username', None)
    context = {
        'id':id,
        'username':username
    }
    return render(request, "Board.html", context=context)


# 졸음 해소 스트레칭 동영상 페이지
def tip(request):
    context={

    }
    return render(request, "tip.html", context=context)


# 카메라 연결
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



'''
        if d_time is not None:
            print(d_time)
            DrowsinessData.objects.create(
                id=id,
                d_time=d_time,
                username=username
            )
            DrowsinessData.save()
'''