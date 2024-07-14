import easyocr
import numpy as np
import random
import cv2
import matplotlib
import time
from datetime import datetime

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image

def ocrTest(fileName, filePath, debug) :
    print("ocrTest IN =================================================")
    print('fileName : ', fileName)
    print('filePath : ', filePath)
    print('debug : ', debug)
    print("============================================================")

    ## 디버그 모드일 시 ocr image 저장 ##
    if debug :
        print("debug IN =================================================")
        start_time = ""
        start_time = time.time()
        reader = easyocr.Reader(['ko'], gpu=False)
        result = reader.readtext(filePath)
        img = cv2.imread(filePath)
        ## 이미지 원본 색상으로 변환 ##
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        ## 이미지 저장 시 폰트 지정
        font = ImageFont.truetype("fonts/NanumSquareRoundB.TTF",20)
        draw = ImageDraw.Draw(img)

        np.random.seed(42)
        COLORS = np.random.randint(0, 255, size=(255, 3),dtype="uint8")

        for i in result :
            x = i[0][0][0]
            y = i[0][0][1]
            w = i[0][1][0] - i[0][0][0]
            h = i[0][2][1] - i[0][1][1]

            color_idx = random.randint(0,255)
            color = [int(c) for c in COLORS[color_idx]]

            draw.rectangle(((x, y), (x+w, y+h)), outline=tuple(color), width=2)
            draw.text((int((x + x + w) / 2) , y-2),str(i[1]), font=font, fill=tuple(color),)

        plt.imshow(img)
        ## 이미지 저장 경로
        ocr_path = 'ocr_images/' + fileName
        ## 이미지 저장
        plt.savefig(ocr_path)

        txts = [line[1] for line in result]
        print("debug txts =================================================")
        print(txts)
        print("============================================================")
        print("time=================================================")
        print("ocrTest elapsed: ", time.time() - start_time)  # seconds
        print("=====================================================")

        ## 저장 경로 및 결과 텍스트 리턴
        result_data = { "txts" : txts, "orc_path" : ocr_path }

    else :
        print("=====================================================")
        print("start_time : ",datetime.now())
        print("=====================================================")
        start_time = ""
        start_time = time.time()
        reader = easyocr.Reader(['ko'], gpu=False)
        result = reader.readtext(filePath)
        print('result : ',result)

        ocr_path = ""
        txts = [line[1] for line in result]
        print("txts=================================================")
        print(txts)
        print("=====================================================")
        print("time=================================================")
        print("ocrTest elapsed: ", time.time() - start_time)  # seconds
        print("=====================================================")
        print("end_time : ",datetime.now())
        print("=====================================================")
        print("now_time : ",datetime.now())

        ## 텍스트 리턴 저장경로는 빈값
        result_data = { "txts" : txts, "orc_path" : ocr_path }

    return result_data