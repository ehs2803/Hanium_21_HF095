import asyncio
import base64
from io import BytesIO
from PIL import Image
import cv2
import websockets
import re, time
import numpy as np

'''
def stringToRGB(base64_string):
    imgdata = base64.b64decode(base64_string)
    dataBytesIO = io.BytesIO(imgdata)
    image = Image.open(dataBytesIO)
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

def getI420FromBase64(codec):
    base64_data = re.sub('^data:image/.+;base64,', '', codec)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    t = time.time()
    print(img.shape)
'''

from io import StringIO
import PIL.Image
def decode_img(img_base64):
    #decode_str = img_base64.decode("base64")
    file_like = StringIO.StringIO(img_base64)
    img = PIL.Image.open(file_like)
    # rgb_img[c, r] is the pixel values.
    rgb_img = img.convert("RGB")
    return rgb_img

def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(BytesIO(imgdata))
    #img =  cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    #print(img.shape)
    cv2.imshow('',img)

# 클라이언트 접속이 되면 호출된다.
async def accept(websocket,path):
    while True:
        data = await websocket.recv();
        if(len(data)<10): continue
        data= data[22:]
        #print(data)
        #stringToRGB(data)
        imgdata = base64.b64decode(str(data))
        image = Image.open(BytesIO(imgdata))
        # img =  cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        # print(img.shape)
        cv2.imshow('', img)


        #image = Image.open(BytesIO(data))  # Image buffer contains the image data from the device.
        #img = imread(io.BytesIO(base64.b64decode(b64_string)))


        # finally convert RGB image to BGR for opencv
        # and save result
        #cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #cv2.imwrite("reconstructed.jpg", cv2_img)
        '''
        #data = data + '=' * (-len(data) % 4)
        temp = base64.urlsafe_b64decode(data)
        encoded_img = np.fromstring(temp, dtype=np.uint8)
        print(encoded_img.shape)
        #img = cv2.imencode(encoded_img, cv2.IMREAD_COLOR)
        cv2.imshow(encoded_img)
        '''





# 웹 소켓 서버 생성.호스트는 localhost에 port는 9998로 생성한다.
start_server = websockets.serve(accept, "localhost", 9998);

# 비동기로 서버를 대기한다.
asyncio.get_event_loop().run_until_complete(start_server);
asyncio.get_event_loop().run_forever();




