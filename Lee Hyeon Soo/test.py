'''
[사용모듈 간단정리]
cv2 : openCV, 웹캠, 영상, 이미지를 다룸
imutils : OpenCV가 제공하는 기능 중에 좀 복잡하고 사용성이 떨어지는 부분을 잘 보완해 주는 패키지.
dlib : 얼굴의 랜드마크(눈, 코, 입, 턱 선, 눈썹 등)찾는기능. 랜드마크를 하기 위해서는 학습된 모델 데이터가 필요
tensorflow : 모델 로드시 사용
numpy : numpy배열 사용
'''
import cv2, dlib
import numpy as np
from imutils import face_utils
#from keras.models import load_model
import tensorflow as tf

#딥러닝 모델의 입력크기 높이:26 너비:34
IMG_SIZE = (34, 26)

# 얼굴 인식용 클래스 생성 (기본 제공되는 얼굴 인식 모델 사용)
detector = dlib.get_frontal_face_detector()
# 인식된 얼굴에서 랜드마크 찾기위한 클래스 생성
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#cnn딥러닝모델 로드하기
model = tf.keras.models.load_model('2018_12_17_22_58_35.h5')
#모델 요약
model.summary()

#매개변수 img프레임에서 눈을 찾아 눈부분의 image와 좌표를 반환하는 함수
def crop_eye(img, eye_points):
  #최솟값: np.amin(fish_data) 최댓값: np.amax(fish_data)
  #eye_points는 얼굴랜드마크좌표(x,y)의 일부값을 가지고 있는 변수이므로 반환값이 x,y로 두개를 반환
  x1, y1 = np.amin(eye_points, axis=0)
  x2, y2 = np.amax(eye_points, axis=0)
  #눈의 정중앙 x,y좌표값을 cx, cy에 저장
  cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

  w = (x2 - x1) * 1.2
  h = w * IMG_SIZE[1] / IMG_SIZE[0]

  #x축의 오차범위와 y축의 오차범위를 각각 저장
  margin_x, margin_y = w / 2, h / 2

  #눈의 중앙값에서 오차범위값을 빼고 더해서 최소, 최대값을 구함
  min_x, min_y = int(cx - margin_x), int(cy - margin_y)
  max_x, max_y = int(cx + margin_x), int(cy + margin_y)

  #np.rint(np.array) : 소숫점 반올림 함수
  #np.array내용의 값들을 소숫점 반올림 후 astype(np.int)를 통해 정수로 변환
  eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
  #프레임 gray의 눈사진 부분을 슬라이싱해서 eye_img에 할당. eye_img : 눈부분 사진
  eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

  return eye_img, eye_rect

# main
#웹캠 ON... 비디오 출력 클래스(cv2.VideoCapture)를 통해 내장 카메라 또는 외장 카메라에서 정보를 받다옴.
#cv2.VideoCapture(index)로 카메라의 장치 번호(ID)와 연결. index는 카메라의 장치번호...
cap = cv2.VideoCapture(0)

#웹캠이 켜져있으면 카메라에서 프레임을 while 반복문으로 지속적으로 받아옴
while cap.isOpened():
  #프레임 읽기 메서드(capture.read)를 이용하여 카메라의 상태(ret) 및 프레임(img_ori)을 받아옴.
  #ret은 카메라의 상태가 저장되며 정상 작동할 경우 True를 반환, 작동하지 않을 경우 False를 반환
  #img_ori에 현재 시점의 프레임이 저장
  ret, img_ori = cap.read()

  # 카메라의 상태가 정상작동 않하면 종료.
  if not ret:
    break

  #cv2.resize(원본 이미지, dsize=(0, 0), 가로비, 세로비, 보간법)로 이미지의 크기를 조절
  #결과 이미지 크기가 (0, 0)으로 크기를 설정하지 않은 경우, fx와 fy를 이용하여 이미지의 비율을 조절
  #ex) fx가 0.3인 경우, 원본 이미지 너비의 0.3배로 변경, fy가 0.7인 경우, 원본 이미지 높이의 0.7배로 변경
  img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5) #프레임을 높이, 너비를 각각 절반으로 줄임.

  #img_ori(웹캠에서읽어온 현재시점의 프레임)을 img에 복사
  img = img_ori.copy()

  #cv2.cvtcolor(원본 이미지, 색상 변환 코드)를 이용하여 이미지의 색상 공간을 변경
  #변환코드(code) cv2.COLOR_BGR2GRAY는 출력영상이 GRAY로 변환
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  #detector에 의해 프레임 안에 얼굴로 판단되는 위치가 넘어오게 되는데 이 값을 faces에 할당
  faces = detector(gray)

  #detector로 찾아낸 얼굴개수는 여러개일 수 있어 for 반복문을 통해 인식된 얼굴 개수만큼 반복
  #만약 웹캠에 사람2명 있다면 print(len(faces))의 출력값은 2
  for face in faces:
    #predictor를 통해 68개의 좌표를 찍음. 위치만 찍는거니까 x좌표, y좌표로 이루어져 이런 [x좌표, y좌표]의 값, 68개가 shapes에 할당
    shapes = predictor(gray, face)
    #얼굴 랜드마크(x, y) 좌표를 NumPy로 변환
    shapes = face_utils.shape_to_np(shapes)

    #crop_eye메소드에 gray프레임과 얼굴랜드마크(x,y)가 numpy로 저장된 shapes에서 오른쪽눈좌표(36~41), 왼쪽눈좌표(42~47) 전달
    #눈사진과 4개의 눈좌표값을 반환받아 각각 변수에 저장.
    eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
    eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

    #왼쪽, 오른쪽 눈 사진을 딥러닝모델에 넣기위해 IMG_SIZE크기로 이미지 크기 조절
    eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
    eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
    #cv2.flip(src, flipCode) : 사진뒤집기 메소드. flipCode=1은 좌우반전
    #추정이지만 cnn모델이 왼쪽눈으로 훈련되있어서 오른쪽눈사진만 좌우반전(flip)시켜서 왼쪽눈처럼 만들어 cnn모델에 사용하기 위한 것 같음.
    eye_img_r = cv2.flip(eye_img_r, flipCode=1)

    #이프로그램을 실행하면 창이 3개 뜬다. 아래 두줄의 코드때문에 2개의 창이 추가로 뜸.
    #왼쪽, 오른쪽부분의 눈사진이 창에 뜸. 삭제해도 되는 코드...
    cv2.imshow('l', eye_img_l)
    cv2.imshow('r', eye_img_r)

    #cnn모델에 입력할 값 전처리작업
    #눈부분 사진을 copy하고 reshape함수를 통해 차원의형태를 변경하고 astype으로 np.float32형태로 만들고 255.0으로 나눠줌
    eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
    eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

    #cnn모델 predict메소드에 가공한 전처리한 눈사진을 넣어 값을 예측.
    #모델출력값은 pred_l, pred_r에 0.0~1.0 사이 값이 저장. 눈을 크게뜰수록 1에 가까워짐.
    pred_l = model.predict(eye_input_l)
    pred_r = model.predict(eye_input_r)

    # visualize
    # 모델출력값이 0이라면 '_ 0.0'으로, 그 외의 숫자라면 '0 0.3'형식으로 문자열 반환하는 문자열을 정의
    state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
    state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'

    # % operator 방식의 문자열 포맷팅
    state_l = state_l % pred_l
    state_r = state_r % pred_r

    #cv2.rectangle(이미지, (x1,y1), (x2,y2), (B,G,R), 두께) 사각형 그림. (x1,y1)의 좌측 상단모서리와 (x2,y2)의 우측 하단모서리
    cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255,255,255), thickness=2)
    cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255,255,255), thickness=2)

    #cv2.putText(이미지, 문자, (x,y), 글꼴, 글자 크기, (B,G,R), 두께)을 이용하여 문자를 그림
    #문자 내용을 가지는 문자열을 (x, y) 위치에 표시
    cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
    cv2.putText(img, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

  # 이미지 표시 함수(cv2.imshow)를 이용하여 특정 윈도우 창에 이미지를 띄웁
  # cv2.imshow(winname, mat)으로 윈도우 창의 제목(winname)과 이미지(mat)를 할당
  cv2.imshow('result', img)

  # 키 입력 대기 함수 Cv2.WaitKey(ms)를 사용해 ms만큼 대기. 'q'입력시 종료
  if cv2.waitKey(1) == ord('q'):
    break

#메모리 해제 메서드(capture.relase)로 카메라 장치에서 받아온 메모리를 해제
cap.release()

#모든 윈도우 창 제거 함수(cv2.destroyAllWindows)를 이용하여 모든 윈도우 창 닫기
cv2.destroyAllWindows()