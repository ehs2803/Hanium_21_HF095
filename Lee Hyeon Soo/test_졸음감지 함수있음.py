import cv2, dlib
import numpy as np
from imutils import face_utils
# from keras.models import load_model
import tensorflow as tf
import time

IMG_SIZE = (34, 26)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

model = tf.keras.models.load_model('2018_12_17_22_58_35.h5')
#model.summary()


def crop_eye(img, eye_points):
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    w = (x2 - x1) * 1.2
    h = w * IMG_SIZE[1] / IMG_SIZE[0]

    margin_x, margin_y = w / 2, h / 2

    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)

    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)
    eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

    return eye_img, eye_rect

#######################################################################################################################
def eyeBlinkCount(pred_r, pred_l):
    global eye_count_min, start
    if pred_r < 0.1 and pred_l < 0.1:
        eye_count_min += 1
        time.sleep(0.15)
    if time.time() - start > 10:
        if eye_count_min < 5:
            start = time.time()
            eye_count_min = 0
            return True
        else:
            start = time.time()
            eye_count_min = 0

def sleepDetection(pred_r, pred_l):
    global  check2, start2
    if pred_r < 0.1 and pred_l < 0.1:
        if check2 == True:
            if time.time() - start2 > 3:
                start2 = time.time()
                check2 = False
                return True
        else:
            check2 = True
            start2 = time.time()
    else:
        check2 = False
        start2 = time.time()
#######################################################################################################################
# main
cap = cv2.VideoCapture(0)
#cap.set(3,1800)
#cap.set(4,1800)
#######################################################################################################################
start=time.time() #시간 측정시작
eye_count_min=0   #1분당안 깜빡임횟수 저장변수
#######################################################################################################################
start2=0
check2=False

while cap.isOpened():
    ret, img_ori = cap.read()

    if not ret:
        break

    img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)

    img = img_ori.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        shapes = predictor(gray, face)
        shapes = face_utils.shape_to_np(shapes)

        eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42])
        eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48])

        eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE)
        eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE)
        eye_img_r = cv2.flip(eye_img_r, flipCode=1)

        eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
        eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

        pred_l = model.predict(eye_input_l)
        pred_r = model.predict(eye_input_r)

        state_min = '%d';
        state_min = state_min % (time.time() - start)
        state_count = '%d';
        state_count = state_count % eye_count_min
        cv2.putText(img, state_min, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, state_count, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
#######################################################################################################################
        check=eyeBlinkCount(pred_r, pred_l)
        if check==True:
            #알림코드 작성...
            print('깜빡임횟수 적음...')

        check=sleepDetection(pred_r, pred_l)
        if check==True:
            #알림코드 작성...
            print('졸음')
#######################################################################################################################
        # visualize
        state_l = 'O %.1f' if pred_l > 0.1 else '- %.1f'
        state_r = 'O %.1f' if pred_r > 0.1 else '- %.1f'

        state_l = state_l % pred_l
        state_r = state_r % pred_r

        cv2.rectangle(img, pt1=tuple(eye_rect_l[0:2]), pt2=tuple(eye_rect_l[2:4]), color=(255, 255, 255), thickness=2)
        cv2.rectangle(img, pt1=tuple(eye_rect_r[0:2]), pt2=tuple(eye_rect_r[2:4]), color=(255, 255, 255), thickness=2)

        cv2.putText(img, state_l, tuple(eye_rect_l[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, state_r, tuple(eye_rect_r[0:2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow('result', img)
    if cv2.waitKey(1) == 48:  # 0입력시 종료
        break
cap.release()
cv2.destroyAllWindows()
'''
#######################################################################################################################
        if pred_r<0.1 and pred_l<0.1:
            eye_count_min+=1
        if time.time()-start>60:
            if eye_count_min<15:
                print('눈깜빡임 횟수 부족!!')
                ##############################
            start=time.time()
            eye_count_min=0

        state_min='%d'; state_min=state_min%(time.time()-start)
        state_count = '%d'; state_count = state_count % eye_count_min
        cv2.putText(img, state_min, (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.putText(img, state_count, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        
        if pred_r<0.1 and pred_l<0.1:
            if check2==True:
                if time.time()-start2>3:
                    start2=time.time()
                    print('sleep detection')
                    check2=False
            else:
                check2=True
                start2=time.time()
        else:
            check2=False
            start2=time.time()
#######################################################################################################################
'''