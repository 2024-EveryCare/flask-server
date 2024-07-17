from openai import OpenAI

def extract_prescription_medications(texts):
    client = OpenAI(api_key="")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts prescription-only medications from given text and outputs them as a list in plain text. 한국어로"},
            {"role": "user", "content": f"Here is text:\n\n{texts}"},
            {"role": "assistant", "content": "Please extract only the prescription-only medications from the above text and list them in plain text."}
        ]
    )

    print(response)

    # Extract and return the response text
    response['choices'][0].message.content

text = """
- Acetaminophen (Tylenol)
- Amoxicillin (Amoxil)
- Ibuprofen (Advil)
- Metformin (Glucophage)
- Lisinopril (Zestril)
- Omeprazole (Prilosec)
- Albuterol (Ventolin)
- Loratadine (Claritin)
- Atorvastatin (Lipitor)
- Cetirizine (Zyrtec)
- Simvastatin (Zocor)
- Azithromycin (Zithromax)
- Losartan (Cozaar)
- Gabapentin (Neurontin)
- Hydrochlorothiazide (Microzide)
"""

result = extract_prescription_medications(text)
print(result)