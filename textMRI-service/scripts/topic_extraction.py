from openai import OpenAI
import json
import sys
import os

# Initialize the OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

# Topic node
# property - name

list_of_topics = []

def get_topic(text):

    assistant = """You are a topic extraction expert. Given a piece of text and list of topics, parse the list of topics first.
    If an element in the list is relevant to the text, then include it in your response. If not, extract unique topics. 
    
    Your results should be returned in an RFC-8259 compliant JSON of the following schema:
    
    {
        name: [String],
    }
    
    """

    prompt = f"Text: {text}, List of Topics: {', '.join(list_of_topics)}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    result = handle_response(result)

    list_of_topics.extend(result["name"])
    
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
    topics = sys.argv[1] 
    content = sys.argv[2]
    try:
        loaded_topics = json.loads(topics)
        if isinstance(loaded_topics, list):
            list_of_topics.extend(loaded_topics)
        else:
            print("Expected topics to be a list")
            sys.exit(2)
    except json.JSONDecodeError:
        print("Invalid JSON data")
        sys.exit(2)

    result = get_topic(content)
    print(json.dumps({
        "topics": result["name"]
    }))
    sys.stdout.flush()

if __name__ == "__main__":
    main()