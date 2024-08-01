import requests
import re

def remove_parentheses(text):
    # 괄호 및 괄호 안의 내용을 제거하는 정규 표현식 사용
    return re.sub(r'\(.*', '', text).strip()

def get_drug_info(item_names):
    # API URL 및 API 키 설정
    api_url = "http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService05/getDrugPrdtPrmsnInq05"
    api_key = "IDPcbgILYcC9dN7AhRfI1bYq0mETbv2lYmV+TqgNSaisuoNC88cAppEZ8bTsoyo7g4yYVYlKUaAbJiRp6m2LFQ=="

    results_name = []  # 제품명 저장 리스트
    # results_SN = []    # 시리얼 넘버 저장 리스트

    for item_name in item_names:
        # 공백과 괄호 이후 텍스트 삭제
        item_name_deleted_blank = item_name.replace(" ", "")
        deleted_blank_final = remove_parentheses(item_name_deleted_blank)



        # API 요청을 위한 파라미터 설정
        params = {
            'serviceKey': api_key,
            'pageNo': 1,
            'numOfRows': 1,
            'type': 'json',
            'item_name': deleted_blank_final  # 전처리된 각 약품명 사용
        }

        try:
            # API 요청
            response = requests.get(api_url, params=params)

            # 응답 확인 및 처리
            if response.status_code == 200:
                data = response.json()
                if 'body' in data and 'items' in data['body'] and data['body']['items']:
                    product_name = data['body']['items'][0]['ITEM_NAME']
                    serial_num = data['body']['items'][0]['ITEM_SEQ']
                    results_name.append(product_name)
                    # results_SN.append(serial_num)
                else:
                    print(f"'{item_name}'에 대한 데이터를 찾을 수 없습니다.")
                    results_name.append(None)
                    #results_SN.append(None)
            else:
                print(f"에러: {response.status_code}")
                print("응답 내용:", response.text)
                results_name.append(None)
                #results_SN.append(None)
        except requests.exceptions.RequestException as e:
            print("오류 발생:", e)
            results_name.append(None)
            #results_SN.append(None)

    return results_name
