import time
def eyeBlinkCount(pred_r, pred_l):
    global eye_count_min, start       #전역변수에 이미 선언되있는 eye_count_min(눈깜빡임횟수), start(시간측정)를 사용
    if pred_r < 0.1 and pred_l < 0.1: #왼쪽, 오른쪽 눈이 모두 감겼다면
        eye_count_min += 1            #깜빡임횟수 1 증가
        time.sleep(0.2)               #한번깜빡일때 민감하게 반응해 2번 횟수가 증가하는 것을 막기위해 0.2초 멈춤
    if time.time() - start > 60:      #시간이 1분이 초과햇을 때
        if eye_count_min < 15:        #눈깜빡임이 15번 미만이라면
            start = time.time()       #시간측정 처음부터 다시시작
            eye_count_min = 0         #눈깜빡임 횟수 0으로 초기화
            return True               #True 반환
        else:                         #눈깜빡임이 15번이상이라면
            start = time.time()       #시간측정 처음부터 다시시작
            eye_count_min = 0         #눈깜빡임 횟수 0으로 초기화