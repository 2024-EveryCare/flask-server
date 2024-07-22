FROM ubuntu:latest
LABEL authors="dokyounglee"

ENTRYPOINT ["top", "-b"]

FROM python:3.12

WORKDIR /flask-server

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && apt-get clean

# EasyOCR 모델 파일 다운로드 및 설정
RUN wget https://github.com/JaidedAI/EasyOCR/releases/download/pre-v1.1.6/craft_mlt_25k.zip
RUN wget https://github.com/JaidedAI/EasyOCR/releases/download/v1.3/korean_g2.zip

# 모델 파일 디렉토리 생성
RUN mkdir -p /.EasyOCR/model

# 모델 파일 압축 해제
RUN unzip craft_mlt_25k.zip -d /.EasyOCR/model/
RUN unzip korean_g2.zip -d /.EasyOCR/model/

WORKDIR /flask-server

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .EasyOCR /flask-server/.EasyOCR

COPY . .

# EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
