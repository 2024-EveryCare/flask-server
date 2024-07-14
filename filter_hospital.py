def filter_hospital_texts(image, ocr_results):
    # "의원"이나 "병원"을 포함하는 텍스트를 필터링하는 기능 추가
    filtered_results = []
    for text_info in ocr_results:
        try:
            text = text_info[1]
            if ('의원' in text or '병원' in text or '외과' in text or '한의원' in text or '종합병원' in text or '치과' in text) and \
                    ('병:의원 처방조제약국' not in text and '병 의원 처방조제악국' not in text and '병의원 처방조제악국' not in text):
                filtered_results.append(text)
        except IndexError:
            continue
    return filtered_results