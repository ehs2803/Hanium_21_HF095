from django.http.response import StreamingHttpResponse
from TaskManager.sleep import Sleep_Detector
from TaskManager.sleep import Blink_Detector
from TaskManager.sleep import sleep_Blink_Detector
from TaskManager.models import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from .models import Questionboard
from .models import CommentQuestionboard
from django.core.paginator import Paginator

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import AuthUser
from django.utils import timezone
# sleep.py 에서 사용자 ID 값 참조를 위한 전역변수
ID = None
USERNAME = None

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
    global errorMsg
    errorMsg=''
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


# 메인 페이지
def main(request):
    id = None
    username = None
    global ID, USERNAME
    if request.session.get('id', None):
        id = request.session.get('id', None)
        username = request.session.get('username', None)
        # DB 활용을 위한 전역변수 저장
        ID = id
        USERNAME = username
    # html로 세션 데이터 전송
    context = {
        'id' : id,            # 사용자 번호
        'username': username  # 사용자 아이디
    }
    return render(request, "main.html", context=context)


# About 페이지
def about(request):
    return render(request, "about.html")


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


# 통합 페이지
def Task_Manager(request):
    return render(request, "TaskManager.html")


# 졸음 감지 페이지
def Drowsiness(request):
    return render(request, "Drowsiness.html")


# 눈 깜빡임 감지 페이지
def Blinking(request):
    return render(request, "Blinking.html")


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
    return render(request, "questionboard.html", context=context)


# 졸음 해소 스트레칭 동영상 페이지
def tip(request):
    return render(request, "tip.html")


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


# Q & A 게시판
def questionboard(request):
    # 사용자정보 로드
    username = None
    if request.session.get('id'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('id'))         # 사용자 이름 저장

    # 페이지정보 로드
    all_questionboard_posts = Questionboard.objects.all().order_by('-id')   # 모든 자유게시판 데이터를 id순으로 가져오기
    paginator = Paginator(all_questionboard_posts, 10)                      # 한 페이지에 10개씩 정렬
    page = int(request.GET.get('p', 1))                                     # p번 페이지 값, p값 없으면 1 반환
    posts = paginator.get_page(page)                                        # p번 페이지 가져오기

    # 자유 게시판 페이지(freeboard.html) 리턴
    return render(request, 'questionboard.html',
                  {'posts': posts, 'username': username})

# Q & A 게시글 쓰기
def questionboard_writing(request):
    # 사용자정보 로드
    username = None
    if request.session.get('id'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('id'))         # 사용자 이름 저장
    # POST 요청시
    if request.method =='POST':
        # 새 게시글 객체 생성
        now = timezone.now()
        formatted_data = now.strftime('%Y-%m-%d %H:%M:%S')
        new_post = Questionboard.objects.create(
            uid=AuthUser.objects.get(id=request.session.get('id', None)),
            title=request.POST['title'],
            contents=request.POST['contents'],
            username=User.objects.get(pk=request.session.get('id')),
            registered_date=formatted_data,
            hits=0,
        )
        return redirect(f'/questionboard_post/{new_post.id}')               # 해당 게시글 페이지로 이동

    # GET 요청시 글쓰기 페이지(writing.html) 리턴
    return render(request, 'questionboard_writing.html', {'username' : username})

# Q & A 게시글 보기
def questionboard_post(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('id'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('id'))         # 사용자 이름 저장

    # 게시글 정보 로드
    post = get_object_or_404(Questionboard, pk=pk)
    # POST 요청시
    if request.method == 'POST':
        # 새 게시글 객체 생성
        now = timezone.now()
        formatted_data = now.strftime('%Y-%m-%d %H:%M:%S')
        new_comment = CommentQuestionboard.objects.create(
            uid=AuthUser.objects.get(id=request.session.get('id', None)),
            create_date=formatted_data,
            username=User.objects.get(pk=request.session.get('id')),
            pid=post.id,
            commets=request.POST['content'],
        )
        return redirect(f'/questionboard_post/{post.id}')  # 해당 게시글 페이지로 이동

    #comments = get_object_or_404(CommentQuestionboard)
    # 해당 게시글 페이지(freeboard_post.html) 리턴
    return render(request, 'questionboard_post.html',
                  {'post' : post, 'username' : username})

# Q & A 게시글 수정
def questionboard_edit(request, pk):
    # 사용자정보 로드
    username = None
    if request.session.get('id'):                                         # 로그인 중이면
        username = User.objects.get(pk=request.session.get('id'))         # 사용자 이름 저장

    # 게시글 정보 로드
    post = Questionboard.objects.get(pk=pk)

    # POST 요청시
    if request.method=="POST":
        post.title = request.POST['title']                                  # 제목 수정 반영
        post.contents = request.POST['contents']                            # 내용 수정 반영
        post.save()                                                         # 수정된 내용 저장
        return redirect(f'/questionboard_post/{pk}')                        # 해당 게시글 페이지로 이동
    # GET 요청시 게시글 수정 페이지(postedit.html) 리턴
    return render(request, 'questionboard_edit.html', {'post':post, 'username' : username})

# Q & A 게시글 삭제
def questionboard_delete(request, pk):
    post = Questionboard.objects.get(id=pk)                                 # 해당 게시글 테이블 저장
    post.delete()                                                           # 해당 게시글 삭제
    return redirect(f'/questionboard')                                      # 자유 게시판 페이지로 이동