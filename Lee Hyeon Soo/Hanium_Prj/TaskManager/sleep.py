from tensorflow.keras.models import load_model
import cv2, dlib, os, time
import numpy as np
from django.conf import settings
from imutils import face_utils
from playsound import playsound

IMG_SIZE = (34, 26)                                                                 # 눈동자 이미지 사이즈 변수
detector = dlib.get_frontal_face_detector()                                         # 정면 얼굴 감지기 로드
model = load_model(os.path.join(settings.BASE_DIR, 'data/detection_model.h5'))  # 눈동자 깜빡임 감지 모델 로드
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')      # 얼굴 랜드마크 좌표값 반환 함수
model2 = load_model(os.path.join(settings.BASE_DIR, 'data/Front_and_Top_2021_07_02.h5'))

# Sleep_Detector 클래스
class Sleep_Detector(object):
    # 생성자
    def __init__(self):
        self.video = cv2.VideoCapture(0)                # 웹캠 연결
        self.success, self.image = self.video.read()    # 프레임 읽어오기 success : 연결 성공 여부   image : 프레임 값

        # 졸음감지 함수 관련변수
        self.start_sleep = 0                            # 졸음감지 시간측정변수
        self.check_sleep = False                        # 눈동자 감김 여부

        # 딥러닝 모델 예측 값 관련 변수
        self.pred_r = 0.0                               # 오른쪽 눈 예측 값
        self.pred_l = 0.0                               # 왼쪽 눈 예측 값

        self.front_back = 0.0
        self.check_sleep_fb = False
        self.start_sleep_fb = 0

    # 소멸자(웹캠 종료)
    def __del__(self):
        self.video.release()                            # 웹캠 연결 해제

    # 매개변수 img 프레임에서 눈을 찾아 눈부분의 image와 좌표를 반환하는 함수
    def crop_eye(self, img, eye_points):
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
    def sleepDetection(self):
        if self.pred_r < 0.1 and self.pred_l < 0.1:                 # 두 눈이 감겼을 때
            if self.check_sleep == True:                            # 졸음이 감지된 적이 있는 경우
                if time.time() - self.start_sleep > 2:              # 2초가 지났을 경우
                    self.start_sleep = time.time()                  # 시간측정 시작
                    self.check_sleep = False                        # 졸음 감지 변수 False 로 변경
                    return True                                     # 졸음이 감지된 상황 -> True 반환
            else:                                                   # 졸음이 감지된 적이 없는 경우
                self.check_sleep = True                             # 졸음 감지 변수를 True 로 변경
                self.start_sleep = time.time()                      # 시간측정 시작
        else:                                                       # 두 눈을 감지 않았을 때
            self.check_sleep = False                                # 졸음 감지 변수를 False 로 변경

    def sleepDetection_frot_back(self):
        if self.front_back < 0.0001:
            if self.check_sleep_fb == True:
                if time.time() - self.start_sleep_fb > 5:
                    self.start_sleep_fb = time.time()
                    self.check_sleep_fb = False
                    return True
            else:
                self.check_sleep_fb = True
                self.start_sleep_fb = time.time()
        else:
            self.check_sleep_fb = False

    # 웹캠 영상 연결 및 프레임 읽기
    # 프레임에 대한 딥러닝 모델 예측
    def get_frame(self):
        self.success, self.image = self.video.read()                            # 프레임 읽어오기
        self.image = cv2.resize(self.image, dsize=(650, 550), fx=0.5, fy=0.5)   # 프레임을 높이, 너비를 각각 절반으로 줄임.

        tempimg = self.image.copy()
        testimg = cv2.resize(tempimg, (150, 150))
        testimg = testimg.copy().reshape((1, 150, 150, 3)).astype(np.float32) / 255.
        self.front_back = model2.predict(testimg)
        print(self.front_back)
        self.get_sleep_front_back()

        # cv2.cvtcolor(원본 이미지, 색상 변환 코드)를 이용하여 이미지의 색상 공간을 변경
        # 변환코드(code) cv2.COLOR_BGR2GRAY는 출력영상이 GRAY로 변환
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

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
            eye_img_l, eye_rect_l = self.crop_eye(gray, shapes[36:42])
            eye_img_r, eye_rect_r = self.crop_eye(gray, shapes[42:48])

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
            self.pred_l = model.predict(eye_input_l)
            self.pred_r = model.predict(eye_input_r)

            # visualize
            # 모델출력값이 0이라면 '_ 0.0'으로, 그 외의 숫자라면 '0 0.3'형식으로 문자열 반환하는 문자열을 정의
            state_l = 'O %.1f' if self.pred_l > 0.1 else '- %.1f'
            state_r = 'O %.1f' if self.pred_r > 0.1 else '- %.1f'

            # % operator 방식의 문자열 포맷팅
            state_l = state_l % self.pred_l
            state_r = state_r % self.pred_r

            # cv2.rectangle(이미지, (x1,y1), (x2,y2), (B,G,R), 두께) 사각형 그림. (x1,y1)의 좌측 상단모서리와 (x2,y2)의 우측 하단모서리
            cv2.rectangle(self.image, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255, 255, 255),
                          thickness=2)
            cv2.rectangle(self.image, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255, 255, 255),
                          thickness=2)

            # cv2.putText(이미지, 문자, (x,y), 글꼴, 글자 크기, (B,G,R), 두께)을 이용하여 문자를 그림
            # 문자 내용을 가지는 문자열을 (x, y) 위치에 표시
            cv2.putText(self.image, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(self.image, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            self.get_sleep()            # 졸음 감지 알림 함수 호출

        # 영상 송출
        ret, jpeg = cv2.imencode('.jpg', self.image)
        return jpeg.tobytes()

    # 졸음감지 알림 함수
    def get_sleep(self):
        if self.sleepDetection():                           # 졸음감지를 하면
            tts_s_path = 'data/sleep_notification.mp3'      # 음성 알림 파일
            playsound(tts_s_path)                           # 음성으로 알림

    def get_sleep_front_back(self):
        if self.sleepDetection_frot_back():
            tts_s_path = 'data/sleep_notification.mp3'  # 음성 알림 파일
            playsound(tts_s_path)  # 음성으로 알림


# Blink_Detector 클래스
class Blink_Detector(object):
    # 생성자
    def __init__(self):
        self.video = cv2.VideoCapture(0)                # 웹캠 연결
        self.success, self.image = self.video.read()    # 프레임 읽어오기  success : 연결 성공 여부  image : 프레임 값

        # 눈깜빡임 감지 함수 관련변수
        self.start_blink = time.time()                  # 눈깜빡임 횟수 시간측정 변수
        self.eye_count_min = 0                          # 눈깜빡임 횟수 저장변수
        self.check_blink = False                        # 눈감김 여부

        self.pred_r = 0.0                               # 오른쪽 눈 예측 값
        self.pred_l = 0.0                               # 왼쪽 눈 예측 값

    # 소멸자(웹캠 종료)
    def __del__(self):
        self.video.release()                            # 웹캠 연결 해제

    # 매개변수 img 프레임에서 눈을 찾아 눈부분의 image와 좌표를 반환하는 함수
    def crop_eye(self, img, eye_points):
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

        return eye_img, eye_rect

    # 눈동자 깜빡임 횟수 측정 및 경고 여부를 반환하는 함수
    def eyeBlinkDetection(self):
        if self.check_blink == True and self.pred_l > 0.9 and self.pred_r > 0.9:    # 눈동자가 감겼으면서 양쪽 눈동자를 뜬경우
            self.eye_count_min += 1                                                 # 눈동자 깜빡임 횟수 변수 1 증가
            self.check_blink = False                                                # 눈동자 감김여부 변수를 False로 변경
        if self.pred_r < 0.1 and self.pred_l < 0.1:                                 # 양쪽 눈동자가 감겼을때
            self.check_blink = True                                                 # 눈동자 감김여부 변수를 True로 변경
        if time.time() - self.start_blink > 60:                                     # 측정시간이 1분(60초)가 지났을 경우
            if self.eye_count_min < 15:                                             # 눈동자 깜빡임 횟수가 15번 미만일 경우
                return True                                                         # True 반환
            else:                                                                   # 눈동자 깜빡임 횟수가 15번 이상일 경우
                self.start_blink = time.time()                                      # 눈동자 깜빡임 시간 측정 시작
                self.eye_count_min = 0                                              # 눈동자 깜빡임 횟수 저장 변수 0으로 초기화

    # 웹캠 영상 연결 및 프레임 읽기
    # 프레임에 대한 딥러닝 모델 예측
    def get_frame(self):
        self.success, self.image = self.video.read()                            # 프레임 읽어오기
        self.image = cv2.resize(self.image, dsize=(650, 550), fx=0.5, fy=0.5)   # 프레임을 높이, 너비를 각각 절반으로 줄임.

        # cv2.cvtcolor(원본 이미지, 색상 변환 코드)를 이용하여 이미지의 색상 공간을 변경
        # 변환코드(code) cv2.COLOR_BGR2GRAY는 출력영상이 GRAY로 변환
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

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
            eye_img_l, eye_rect_l = self.crop_eye(gray, shapes[36:42])
            eye_img_r, eye_rect_r = self.crop_eye(gray, shapes[42:48])

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
            self.pred_l = model.predict(eye_input_l)
            self.pred_r = model.predict(eye_input_r)

            self.blink_count()              # 눈동자 깜빡임 횟수 부족 알림 함수 호출

            # visualize
            # 모델출력값이 0이라면 '_ 0.0'으로, 그 외의 숫자라면 '0 0.3'형식으로 문자열 반환하는 문자열을 정의
            state_l = 'O %.1f' if self.pred_l > 0.1 else '- %.1f'
            state_r = 'O %.1f' if self.pred_r > 0.1 else '- %.1f'

            # % operator 방식의 문자열 포맷팅
            state_l = state_l % self.pred_l
            state_r = state_r % self.pred_r

            # cv2.rectangle(이미지, (x1,y1), (x2,y2), (B,G,R), 두께) 사각형 그림. (x1,y1)의 좌측 상단모서리와 (x2,y2)의 우측 하단모서리
            cv2.rectangle(self.image, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255, 255, 255),
                          thickness=2)
            cv2.rectangle(self.image, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255, 255, 255),
                          thickness=2)

            # cv2.putText(이미지, 문자, (x,y), 글꼴, 글자 크기, (B,G,R), 두께)을 이용하여 문자를 그림
            # 문자 내용을 가지는 문자열을 (x, y) 위치에 표시
            cv2.putText(self.image, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(self.image, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 임시 코드
        # 초, 눈깜빡임 횟수 출력에 대한 문자열 정의
        state_min = '%d'
        state_count = '%d'
        # % operator 방식의 문자열 포맷팅
        state_min = state_min % (time.time() - self.start_blink)
        state_count = state_count % self.eye_count_min

        # 1분을 초로 출력
        cv2.putText(self.image, state_min, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # 1분동안 눈동자 깜빡임 횟수 출력
        cv2.putText(self.image, state_count, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # 영상 송출
        ret, jpeg = cv2.imencode('.jpg', self.image)
        return jpeg.tobytes()

    # 눈동자 깜빡임 횟수 부족 알림 함수
    def blink_count(self):
        if self.eyeBlinkDetection():                                     # 눈동자 깜빡임의 횟수가 적으면
            tts_b_path = 'data/blink_count' + str(self.eye_count_min) + '.mp3'      # 알림 음성 파일
            playsound(tts_b_path)                                        # 음성으로 알림
            self.start_blink = time.time()                               # 눈동자 깜빡임 시간 측정 시작
            self.eye_count_min = 0                                       # 눈동자 깜빡임 횟수 저장 변수 0으로 초기화

# sleep_Blink_Detector 클래스 (통합 기능)
class sleep_Blink_Detector(object):
    # 생성자
    def __init__(self):
        self.video = cv2.VideoCapture(0)                # 웹캠 연결
        self.success, self.image = self.video.read()    # 프레임 읽어오기  success : 연결 성공 여부  image : 프레임 값

        # 졸음감지 함수 관련변수
        self.start_sleep = 0  # 졸음감지 시간측정변수
        self.check_sleep = False  # 눈동자 감김 여부

        # 눈깜빡임 감지 함수 관련변수
        self.start_blink = time.time()                  # 눈깜빡임 횟수 시간측정 변수
        self.eye_count_min = 0                          # 눈깜빡임 횟수 저장변수
        self.check_blink = False                        # 눈감김 여부

        self.pred_r = 0.0                               # 오른쪽 눈 예측 값
        self.pred_l = 0.0                               # 왼쪽 눈 예측 값

        self.front_back = 0.0
        self.check_sleep_fb = False
        self.start_sleep_fb = 0

    # 소멸자(웹캠 종료)
    def __del__(self):
        self.video.release()                            # 웹캠 연결 해제

    # 매개변수 img 프레임에서 눈을 찾아 눈부분의 image와 좌표를 반환하는 함수
    def crop_eye(self, img, eye_points):
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

        return eye_img, eye_rect

    # 졸음 감지 함수
    # 졸음이 감지되면 True 를 반환하면서 함수를 종료함
    def sleepDetection(self):
        if self.pred_r < 0.1 and self.pred_l < 0.1:                 # 두 눈이 감겼을 때
            if self.check_sleep == True:                            # 졸음이 감지된 적이 있는 경우
                if time.time() - self.start_sleep > 2:              # 2초가 지났을 경우
                    self.start_sleep = time.time()                  # 시간측정 시작
                    self.check_sleep = False                        # 졸음 감지 변수 False 로 변경
                    return True                                     # 졸음이 감지된 상황 -> True 반환
            else:                                                   # 졸음이 감지된 적이 없는 경우
                self.check_sleep = True                             # 졸음 감지 변수를 True 로 변경
                self.start_sleep = time.time()                      # 시간측정 시작
        else:                                                       # 두 눈을 감지 않았을 때
            self.check_sleep = False                                # 졸음 감지 변수를 False 로 변경

    def sleepDetection_frot_back(self):
        if self.front_back < 0.0001:
            if self.check_sleep_fb == True:
                if time.time() - self.start_sleep_fb > 5:
                    self.start_sleep_fb = time.time()
                    self.check_sleep_fb = False
                    return True
            else:
                self.check_sleep_fb = True
                self.start_sleep_fb = time.time()
        else:
            self.check_sleep_fb = False

    # 눈동자 깜빡임 횟수 측정 및 경고 여부를 반환하는 함수
    def eyeBlinkDetection(self):
        if self.check_blink == True and self.pred_l > 0.9 and self.pred_r > 0.9:    # 눈동자가 감겼으면서 양쪽 눈동자를 뜬경우
            self.eye_count_min += 1                                                 # 눈동자 깜빡임 횟수 변수 1 증가
            self.check_blink = False                                                # 눈동자 감김여부 변수를 False로 변경
        if self.pred_r < 0.1 and self.pred_l < 0.1:                                 # 양쪽 눈동자가 감겼을때
            self.check_blink = True                                                 # 눈동자 감김여부 변수를 True로 변경
        if time.time() - self.start_blink > 60:                                     # 측정시간이 1분(60초)가 지났을 경우
            if self.eye_count_min < 15:                                             # 눈동자 깜빡임 횟수가 15번 미만일 경우
                return True                                                         # True 반환
            else:                                                                   # 눈동자 깜빡임 횟수가 15번 이상일 경우
                self.start_blink = time.time()                                      # 눈동자 깜빡임 시간 측정 시작
                self.eye_count_min = 0                                              # 눈동자 깜빡임 횟수 저장 변수 0으로 초기화

    # 웹캠 영상 연결 및 프레임 읽기
    # 프레임에 대한 딥러닝 모델 예측
    def get_frame(self):
        self.success, self.image = self.video.read()                            # 프레임 읽어오기
        self.image = cv2.resize(self.image, dsize=(650, 550), fx=0.5, fy=0.5)   # 프레임을 높이, 너비를 각각 절반으로 줄임.

        tempimg = self.image.copy()
        testimg = cv2.resize(tempimg, (150, 150))
        testimg = testimg.copy().reshape((1, 150, 150, 3)).astype(np.float32) / 255.
        self.front_back = model2.predict(testimg)
        self.get_sleep_front_back()

        # cv2.cvtcolor(원본 이미지, 색상 변환 코드)를 이용하여 이미지의 색상 공간을 변경
        # 변환코드(code) cv2.COLOR_BGR2GRAY는 출력영상이 GRAY로 변환
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

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
            eye_img_l, eye_rect_l = self.crop_eye(gray, shapes[36:42])
            eye_img_r, eye_rect_r = self.crop_eye(gray, shapes[42:48])

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
            self.pred_l = model.predict(eye_input_l)
            self.pred_r = model.predict(eye_input_r)

            self.blink_count()              # 눈동자 깜빡임 횟수 부족 감지 함수 호출
            self.get_sleep()                # 졸음 감지 함수 호출

            # visualize
            # 모델출력값이 0이라면 '_ 0.0'으로, 그 외의 숫자라면 '0 0.3'형식으로 문자열 반환하는 문자열을 정의
            state_l = 'O %.1f' if self.pred_l > 0.1 else '- %.1f'
            state_r = 'O %.1f' if self.pred_r > 0.1 else '- %.1f'

            # % operator 방식의 문자열 포맷팅
            state_l = state_l % self.pred_l
            state_r = state_r % self.pred_r

            # cv2.rectangle(이미지, (x1,y1), (x2,y2), (B,G,R), 두께) 사각형 그림. (x1,y1)의 좌측 상단모서리와 (x2,y2)의 우측 하단모서리
            cv2.rectangle(self.image, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255, 255, 255),
                          thickness=2)
            cv2.rectangle(self.image, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255, 255, 255),
                          thickness=2)

            # cv2.putText(이미지, 문자, (x,y), 글꼴, 글자 크기, (B,G,R), 두께)을 이용하여 문자를 그림
            # 문자 내용을 가지는 문자열을 (x, y) 위치에 표시
            cv2.putText(self.image, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(self.image, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 임시 코드
        # 초, 눈깜빡임 횟수 출력에 대한 문자열 정의
        state_min = '%d'
        state_count = '%d'
        # % operator 방식의 문자열 포맷팅
        state_min = state_min % (time.time() - self.start_blink)
        state_count = state_count % self.eye_count_min

        # 1분을 초로 출력
        cv2.putText(self.image, state_min, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        # 1분동안 눈동자 깜빡임 횟수 출력
        cv2.putText(self.image, state_count, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # 영상 송출
        ret, jpeg = cv2.imencode('.jpg', self.image)
        return jpeg.tobytes()

    # 눈동자 깜빡임 횟수 부족 알림 함수
    def blink_count(self):
        if self.eyeBlinkDetection():  # 눈동자 깜빡임의 횟수가 적으면
            tts_b_path = 'data/blink_count' + str(self.eye_count_min) + '.mp3'  # 알림 음성 파일
            playsound(tts_b_path)  # 음성으로 알림
            self.start_blink = time.time()  # 눈동자 깜빡임 시간 측정 시작
            self.eye_count_min = 0  # 눈동자 깜빡임 횟수 저장 변수 0으로 초기화

    # 졸음감지 알림 함수
    def get_sleep(self):
        if self.sleepDetection():                           # 졸음감지를 하면
            tts_s_path = 'data/sleep_notification.mp3'      # 음성 알림 파일
            playsound(tts_s_path)                           # 음성으로 알림

    def get_sleep_front_back(self):
        if self.sleepDetection_frot_back():
            tts_s_path = 'data/sleep_notification.mp3'  # 음성 알림 파일
            playsound(tts_s_path)  # 음성으로 알림