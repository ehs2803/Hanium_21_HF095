import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import threading
from playsound import playsound
import time
import TaskManager.sleep
from tensorflow.keras.models import load_model
import cv2, dlib, os, time
import numpy as np

from imutils import face_utils
from playsound import playsound

from django.conf import settings
from django.db import connection
from django.utils import timezone

from TaskManager import views

IMG_SIZE = (34, 26)                                                                 # 눈동자 이미지 사이즈 변수
detector = dlib.get_frontal_face_detector()                                         # 정면 얼굴 감지기 로드
model = load_model(os.path.join(settings.BASE_DIR, 'data/detection_model.h5'))  # 눈동자 깜빡임 감지 모델 로드
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')      # 얼굴 랜드마크 좌표값 반환 함수
model2 = load_model(os.path.join(settings.BASE_DIR, 'data/Front_and_Top_2021_07_02.h5'))

frame = None
check=False
thread_flag = False


# 졸음감지 함수 관련변수
start_sleep = 0                            # 졸음감지 시간측정변수
check_sleep = False                        # 눈동자 감김 여부
# 딥러닝 모델 예측 값 관련 변수
pred_r = 0.0                               # 오른쪽 눈 예측 값
pred_l = 0.0                               # 왼쪽 눈 예측 값
front_back = 0.0
check_sleep_fb = False
start_sleep_fb = 0


# 매개변수 img 프레임에서 눈을 찾아 눈부분의 image와 좌표를 반환하는 함수
def crop_eye(img, eye_points):
    # 최솟값: np.amin(fish_data) 최댓값: np.amax(fish_data)
    # eye_points 는 얼굴랜드마크좌표(x,y)의 일부값을 가지고 있는 변수이므로 반환값이 x,y로 두개를 반환
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)

    # 눈의 정중앙 x,y 좌표 값을 cx, cy에 저장
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    # w : 눈동자의 너비, h : 눈동자의 높이
    w = (x2 - x1) * 1.2
    h = w * IMG_SIZE[1] / IMG_SIZE[0]

    # x축의 오차범위와 y축의 오차범위를 각각 저장
    margin_x, margin_y = w / 2, h / 2

    # 눈의 중앙값에서 오차범위값을 빼고 더해서 최소, 최대값을 구함
    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)

    # np.rint(np.array) : 소숫점 반올림 함수
    # np.array 내용의 값들을 소숫점 반올림 후 astype(np.int)를 통해 정수로 변환
    # eye_rect : 사각형을 그리는 좌표값
    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
    # 프레임 gray 의 눈사진 부분을 슬라이싱해서 eye_img 에 할당. eye_img : 눈부분 사진
    eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

    # 눈부분 사진과 눈부분 사각형 좌표값 반환
    return eye_img, eye_rect


# 졸음 감지 함수
# 졸음이 감지되면 True 를 반환하면서 함수를 종료함
def sleepDetection():
    global pred_l, pred_r, check_sleep, start_sleep
    if pred_r < 0.1 and pred_l < 0.1:  # 두 눈이 감겼을 때
        if check_sleep == True:  # 졸음이 감지된 적이 있는 경우
            if time.time() - start_sleep > 2:  # 2초가 지났을 경우
                start_sleep = time.time()  # 시간측정 시작
                check_sleep = False  # 졸음 감지 변수 False 로 변경
                return True  # 졸음이 감지된 상황 -> True 반환
        else:  # 졸음이 감지된 적이 없는 경우
            check_sleep = True  # 졸음 감지 변수를 True 로 변경
            start_sleep = time.time()  # 시간측정 시작
    else:  # 두 눈을 감지 않았을 때
        check_sleep = False  # 졸음 감지 변수를 False 로 변경


def sleepDetection_frot_back():
    global front_back, check_sleep_fb, start_sleep_fb
    if front_back < 0.0001:
        if check_sleep_fb == True:
            if time.time() - start_sleep_fb > 5:
                start_sleep_fb = time.time()
                check_sleep_fb = False
                return True
        else:
            check_sleep_fb = True
            start_sleep_fb = time.time()
    else:
        check_sleep_fb = False

# 졸음감지 알림 함수
def get_sleep():
    if sleepDetection():                           # 졸음감지를 하면
        tts_s_path = 'data/sleep_notification.mp3'      # 음성 알림 파일
        playsound(tts_s_path)      # 음성으로 알림
        # DB에 정보 삽입
        cursor = connection.cursor()
        now=timezone.localtime()
        formatted_data = now.strftime('%Y=%m-%d %H:%M:%S')
        cursor.execute('insert into drowsiness_data values(%s,%s,%s)',
                        (views.ID, formatted_data, views.USERNAME))
        connection.commit()
        connection.close()

def get_sleep_front_back():
    if sleepDetection_frot_back():
        tts_s_path = 'data/sleep_notification.mp3'      # 음성 알림 파일
        playsound(tts_s_path)      # 음성으로 알림

        cursor = connection.cursor()
        now=timezone.localtime()
        formatted_data = now.strftime('%Y=%m-%d %H:%M:%S')
        cursor.execute('insert into drowsiness_data values(%s,%s,%s)',
                        (views.ID, formatted_data, views.USERNAME))
        connection.commit()
        connection.close()

def test():
    time.sleep(5)
    global frame, pred_l, pred_r, detector, model, model2, front_back, predictor
    while True:
        if thread_flag==True:
            break

        tempimg = frame.copy()
        testimg = cv2.resize(tempimg, (150, 150))
        testimg = testimg.copy().reshape((1, 150, 150, 3)).astype(np.float32) / 255.
        front_back = model2.predict(testimg)
        # print(self.front_back)
        get_sleep_front_back()

        # cv2.cvtcolor(원본 이미지, 색상 변환 코드)를 이용하여 이미지의 색상 공간을 변경
        # 변환코드(code) cv2.COLOR_BGR2GRAY는 출력영상이 GRAY로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detector에 의해 프레임 안에 얼굴로 판단되는 위치가 넘어오게 되는데 이 값을 faces에 할당
        faces = detector(gray)

        # detector로 찾아낸 얼굴개수는 여러개일 수 있어 for 반복문을 통해 인식된 얼굴 개수만큼 반복
        # 만약 웹캠에 사람2명 있다면 print(len(faces))의 출력값은 2
        for face in faces:
            # predictor를 통해 68개의 좌표를 찍음. 위치만 찍는거니까 x좌표, y좌표로 이루어져 이런 [x좌표, y좌표]의 값, 68개가 shapes에 할당
            shapes = predictor(gray, face)
            # 얼굴 랜드마크(x, y) 좌표를 NumPy로 변환
            shapes = face_utils.shape_to_np(shapes)

            # eye_img : 눈동자 사진 eye_rect : 눈동자 좌표값
            eye_img_l, eye_rect_l = crop_eye(gray, shapes[36:42])
            eye_img_r, eye_rect_r = crop_eye(gray, shapes[42:48])

            # 왼쪽, 오른쪽 눈 사진을 딥러닝모델에 넣기위해 IMG_SIZE크기로 이미지 크기 조절
            eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
            eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)

            # cv2.flip(src, flipCode) : 사진뒤집기 메소드. flipCode=1은 좌우반전
            # 추정이지만 cnn모델이 왼쪽눈으로 훈련되있어서 오른쪽눈사진만 좌우반전(flip)시켜서 왼쪽눈처럼 만들어 cnn모델에 사용하기 위한 것 같음.
            eye_img_r = cv2.flip(eye_img_r, flipCode=1)

            # cnn모델에 입력할 값 전처리작업
            # 눈부분 사진을 copy하고 reshape함수를 통해 차원의형태를 변경하고 astype으로 np.float32형태로 만들고 255.0으로 나눠줌
            eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
            eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

            # cnn모델 predict메소드에 가공한 전처리한 눈사진을 넣어 값을 예측.
            # 모델출력값은 pred_l, pred_r에 0.0~1.0 사이 값이 저장. 눈을 크게뜰수록 1에 가까워짐.
            pred_l = model.predict(eye_input_l)
            pred_r = model.predict(eye_input_r)
            print(pred_r)
            # visualize
            # 모델출력값이 0이라면 '_ 0.0'으로, 그 외의 숫자라면 '0 0.3'형식으로 문자열 반환하는 문자열을 정의
            state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
            state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'

            get_sleep()  # 졸음 감지 알림 함수 호출
        print(555)

class ChatConsumer(AsyncWebsocketConsumer):
    # connect to Websocket
    async def connect(self):
        global  check, thread_flag
        check = False
        thread_flag = False
        await self.accept()

    async def disconnect(self, code):
        global thread_flag
        thread_flag=True
        print('======================================')

    async def receive(self, text_data):
        global check
        if check==False:
            check=True
            t = threading.Thread(target=test, daemon=True)
            t.start()

        global frame
        data = text_data
        if (len(data) > 10):
            data = data[22:]
            temp = base64.urlsafe_b64decode(data)
            img = Image.open(BytesIO(temp))
            img = np.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = cv2.resize(img, dsize=(650, 550), fx=0.5, fy=0.5)  # 프레임을 높이, 너비를 각각 절반으로 줄임.
            frame = img
            #print(type(img))
