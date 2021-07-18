from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from TaskManager.sleep import Sleep_Detector
from TaskManager.sleep import Blink_Detector
from TaskManager.sleep import sleep_Blink_Detector

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('signup')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


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

def tip(req):
    context={

    }
    return render(req, "tip.html", context=context)

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
