from openai import OpenAI
import json
import sys
import os

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

def get_knowledge_type(text):
    # modified prompt to fit JSON input
    assistant = """You are a knowledge classifier expert. Given a JSON object with the speaker, turn and content, classify contents combined as procedural,
    declarative, or conditional. Your results should be returned in an RFC-8259 compliant JSON of the
    following schema:
    
    {
        type: String,
        explanation: String
    }
    
    """

    prompt = f"{text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    result = handle_response(result)
    return result


def is_valid_json(json_str):
    try:
        json_object = json.loads(json_str)
    except ValueError as e:
        return False, str(e)
    return True, json_object

def handle_response(response_text):
    # Remove any extraneous text or formatting
    response_text = response_text.strip()

    if response_text.startswith('```json'):
        response_text = response_text[7:]
    if response_text.endswith('```'):
        response_text = response_text[:-3]
        
    response_text = response_text.strip()
    # Validate JSON
    is_valid, result = is_valid_json(response_text)
    if is_valid:
        return result
    else:
        raise ValueError(f"Invalid JSON response: {result}")

# text should be the all of transcipt content
def main():
    text= sys.argv[1]
    results = get_knowledge_type(text)
    print(json.dumps(results))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
