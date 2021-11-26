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

def test():
    time.sleep(5)
    global frame
    cnt=0
    while True:
        if thread_flag==True:
            break
        cnt+=1
        #print(cnt)
        testimg = cv2.resize(frame, (150, 150))
        testimg = testimg.copy().reshape((1, 150, 150, 3)).astype(np.float32) / 255.
        front_back = model2.predict(testimg)
        print(front_back)
        if cnt==300000:
            tts_s_path = 'data/sleep_notification.mp3'  # 음성 알림 파일
            playsound(tts_s_path)  # 음성으로 알림

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
