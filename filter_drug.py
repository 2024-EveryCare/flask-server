"""
def filter_drug_texts(ocr_results):
    # "정", "액", "시럽", "캡슐" 을 포함하는 텍스트만 선택하여 리스트에 추가
    filtered_results = []
    for text_info in ocr_results:
        try:
            text = text_info[1]
            if '정' in text or '액' in text or '시럽' in text or '캡슐' in text:
                filtered_results.append(text)
        except IndexError:
            continue
    return filtered_results
"""

"""
import re

def filter_drug_texts(ocr_results):
    filtered_results = []
    pattern = r".*정\w*$"  # 정규표현식 패턴

    for text_info in ocr_results:
        try:
            text = text_info[1]
            if re.match(pattern, text):
                filtered_results.append(text)
        except IndexError:
            continue

    return filtered_results

"""

def filter_drug_texts(ocr_results):
    # 필터링할 키워드 리스트
    filter_keywords = ['정', '액', '시럽', '캡슐','패취', '비오플산','비오', '우리들', '팜젠','아세틸', '그램', '밀리그램']
    additional_filters = ['환 자 정 보', '안정제', '항정신', '정신', '1정', '2정','3정', '씩', '정보', '환자정보', '정상', '정습기', '정장제', '정사각형','패취제','향', '색']

    filtered_results = []
    for text_info in ocr_results:
        try:
            text = text_info[1]
            # 필터링할 키워드가 포함되는지 확인
            if any(keyword in text for keyword in filter_keywords):
                # additional_filters에 포함된 문자열이 하나라도 부분적으로라도 포함되지 않도록 확인
                if not any(is_partial_match(text, filter_word) for filter_word in additional_filters):
                    filtered_results.append(text)
        except IndexError:
            continue

    return filtered_results

def is_partial_match(full_text, partial_text):
    # partial_text가 full_text의 일부분으로 포함되어 있는지 확인
    return partial_text in full_text