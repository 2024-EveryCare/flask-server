import openai

# OpenAI API 키 설정
openai.api_key = 'myapi'

def extract_drug_names(texts):
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=f"다음 텍스트에서 약품명을 찾아주세요:\n\n{texts}\n\n약품명:",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5
    )

    # 결과에서 약품명 추출
    drug_names = response.choices[0].text.strip()
    return drug_names
