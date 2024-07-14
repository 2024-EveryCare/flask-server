from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import easyocr
import cv2
import uuid

from drug_search_api import get_drug_info
from perform_ocr import save_image # ocr 로직 가져오기
from perform_ocr import draw_bounding_boxes # ocr 로직 가져오기
from drug_gpt import extract_drug_names #gpt 사용하여 필터링 로직 가져오기
from perform_ocr import perform_ocr # ocr 로직 가져오기
from filter_drug import filter_drug_texts  # 필터링 로직 가져오기
from filter_hospital import filter_hospital_texts  # 필터링 로직 가져오기

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    # 허용된 파일 확장자인지 확인
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return '안녕하세요, OCR 서버입니다!'

@app.route('/api/v1/medicines/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "파일이 없습니다"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "선택된 파일이 없습니다"}), 400

    if 'userID' not in request.form:
        return jsonify({"error": "userID가 없습니다"}), 400

    user_id = request.form['userID']

    if file and allowed_file(file.filename):
        # 고유 ResultID 생성
        result_id = str(uuid.uuid4())

        # 파일 저장
        file_ext = file.filename.rsplit('.', 1)[1].lower()  # 파일 확장자 추출
        filename = secure_filename(f"{result_id}.{file_ext}")  # resultID로 파일명 생성
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # OCR 처리
        image, ocr_result, texts = perform_ocr(file_path)

        # 디버깅: OCR 결과 출력
        ## print("OCR Result:", texts)
        ## gpt_drug_names = extract_drug_names(texts)
        ## print(gpt_drug_names)

        # 바운딩 박스 그리기
        annotated_image = draw_bounding_boxes(image, ocr_result)

        # 사진 저장하기
        save_image(annotated_image)

        # 약품명 필터링 결과 얻기
        item_names = filter_drug_texts(ocr_result)

        # print("Filter Result:", item_names)

        # 약품명 api를 통한 조회
        drug_names, serial_num = get_drug_info(item_names)

        # 병원명 필터링 결과 얻기
        hospital_names = filter_hospital_texts(image, ocr_result)

        # OCR 결과와 파일 경로 반환
        return jsonify({
            "code": "A001",
            "status": "200",
            "message": "사진 등록 성공",
            "resultID": result_id,
            "userID": user_id,
            "drugName": drug_names,
            "hospital": hospital_names,
            "drug_serialNum" : serial_num
        })

    return jsonify({"error": "허용되지 않는 파일 형식입니다"}), 400

if __name__ == '__main__':
    app.run(debug=False)