import asyncio
import base64
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import cv2
# 웹 소켓 모듈을 선언한다.
import websockets


# 클라이언트 접속이 되면 호출된다.
async def accept(websocket, path):
    while True:
        # 클라이언트로부터 메시지를 대기한다.
        data = await websocket.recv()
        if(len(data)<10): continue
        print('=======================================================')
        print('type of data :', type(data))
        # print("receive : " + data)
        print()
        # 클라인언트로 echo를 붙여서 재 전송한다.
        await websocket.send("echo : " + data)

        # 데이터 슬라이싱
        data = data[22:]
        temp = base64.urlsafe_b64decode(data)
        print('=======================================================')
        print('type of temp :', type(temp))
        # print(temp)

        img = Image.open(BytesIO(temp))
        #plt.imshow(img)
        #plt.show()
        cv2.imshow('a',img)


# 웹 소켓 서버 생성.호스트는 localhost에 port는 9998로 생성한다.
start_server = websockets.serve(accept, "localhost", 9998)

# 비동기로 서버를 대기한다.
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()