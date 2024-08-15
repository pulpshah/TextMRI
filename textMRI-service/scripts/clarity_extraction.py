from openai import OpenAI
import json
import sys
import os

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

def get_readability(text):

    assistant = """You are a readability scorer expert. Given a piece of text, evaluate its readability on a scale of [0.0, 1.0), with
    1.0 being readable by everyone and 0.0 being readable by no one.
    
    Your results should be returned in an RFC-8259 compliant JSON of the following schema:
    
    {
        score: float,
        explanation: String
    }
    
    """

    prompt = f"Text: {text}"

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

def get_grammar(text):

    assistant = """You are a grammar scorer expert. Given a piece of text, evaluate its use and efficacy of grammar on a scale of [0.0, 1.0), with
    1.0 being highly effective usage of of grammar and 0.0 being poor use of grammar with little efficacy.
    
    Your results should be returned in an RFC-8259 compliant JSON of the following schema:
    
    {
        score: float,
        explanation: String
    }
    
    """

    prompt = f"Text: {text}"

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

def main():
    content = sys.argv[1]
    readability = get_readability(content)
    grammar = get_grammar(content)
    
    readability_score = readability['score']
    readability_expl = readability['explanation']
    grammar_score = grammar['score']
    grammar_expl = grammar['explanation']
    score = readability_score * grammar_score

    clarity=[{
        "score" : score,
        "readability_score": readability_score,
        "readability_expl": readability_expl,
        "grammar_score": grammar_score,
        "grammar_expl": grammar_expl
    }]

    print(json.dumps(clarity))
    sys.stdout.flush()

if __name__ == "__main__":
    main()


