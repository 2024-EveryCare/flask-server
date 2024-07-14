"""
import easyocr
import cv2

def perform_ocr(file_path):
    # OCR 리더 초기화 (한국어 설정, GPU 사용 안 함)
    reader = easyocr.Reader(['ko'], gpu=False)

    # 이미지 읽기
    image = cv2.imread(file_path)

    # OpenCV 이미지를 RGB 형식으로 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # OCR 처리
    result = reader.readtext(image_rgb)

    return result
"""

import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image
import os

def perform_ocr(file_path):
    # OCR 리더 초기화 (한국어 설정, GPU 사용 안 함)
    reader = easyocr.Reader(['ko'], gpu=False)

    # 이미지 읽기
    image = cv2.imread(file_path)

    # OpenCV 이미지를 RGB 형식으로 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # OCR 처리
    result = reader.readtext(image_rgb)

    # 텍스트만 추출
    texts = [text for _, text, _ in result]
    combined_text = ' '.join(texts)


    return image, result, combined_text

def draw_bounding_boxes(image, result, font_path='fonts/NanumGothicBold.ttf'):
    # Convert image to PIL format for drawing
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    font = ImageFont.truetype(font_path, 18)
    draw = ImageDraw.Draw(image_pil)

    # Draw bounding boxes and text
    for i in result:
        x = i[0][0][0]
        y = i[0][0][1]
        w = i[0][1][0] - i[0][0][0]
        h = i[0][2][1] - i[0][1][1]

        draw.rectangle(((x, y), (x + w, y + h)), outline="blue", width=2)
        draw.text((int((x + x + w) / 2), y - 20), str(i[1]), font=font, fill="red")

    return image_pil

def save_image(image, output_dir='ocr_images'):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Save the result image with a unique name
    for i in range(1, 10000):
        save_path = os.path.join(output_dir, f"result{i}.jpg")
        try:
            with open(save_path, 'xb') as f:
                image.save(save_path)
                print(f"Image saved to {save_path}")
                break
        except FileExistsError:
            continue



