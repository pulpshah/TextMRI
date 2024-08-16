from openai import OpenAI
import json
import sys
import os

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

# Cohesion node
# property - topic_relevancy_score, topic_relevancy_explanation, topic_continuity_score, topic_continuity_explanation, topic_transition_score, topic_transition_explanation, score


def get_topic_relevancy(comment, previous_comment1, previous_comment2, previous_comment3, previous_comment4, previous_comment5):

    assistant = """You are a topic relevancy expert. Given a piece of text and the previous comments, evaluate the relevancy of the current
    topic or subject matter to the immediate context or discussion in the range [0.0, 1.0).
    
    Your results should be returned in an RFC-8259 compliant JSON of the following schema:
    
    {
        score: float,
        explanation: String
    }
    
    """

    prompt = f"Comment: {comment}, Previous Comment 1: {previous_comment1}, Previous Comment 2: {previous_comment2}, Previous Comment 3: {previous_comment3}, Previous Comment 4: {previous_comment4}, Previous Comment 5: {previous_comment5}"

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

def get_topic_continuity(comment):

    assistant = """You are a topic continuity expert. Given a piece of text, evaluate the smoothness and logical flow of topics
    or themes from one point to another in the text in the range [0.0, 1.0). 
    
    Your results should be returned in an RFC-8259 compliant JSON of the following schema:
    
    {
        score: float,
        explanation: String
    }
    
    """

    prompt = f"Comment: {comment}"

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

def get_topic_transition(comment):

    assistant = """You are a topic transition expert. Given a piece of text, evaluate the effectivness of transitions between different
    topics or ideas in the text in the range [0.0, 1.0). 
    
    Your results should be returned in an RFC-8259 compliant JSON of the following schema:
    
    {
        score: float,
        explanation: String
    }
    
    """

    prompt = f"Comment: {comment}"

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
def get_cohesion(content, turn_number, previous_comments):
    if turn_number <= 5:
        topic_relevancy = {
            "score": 0.75,
            "explanation": "No previous 5 turns"
        }
    else:
        topic_relevancy = get_topic_relevancy(content, *previous_comments)

    topic_continuity = get_topic_continuity(content)
    topic_transition = get_topic_transition(content)

    return {
        "topic_relevancy_score": topic_relevancy['score'],
        "topic_relevancy_explanation": topic_relevancy['explanation'],
        "topic_continuity_score": topic_continuity['score'],
        "topic_continuity_explanation": topic_continuity['explanation'],
        "topic_transition_score": topic_transition['score'],
        "topic_transition_explanation": topic_transition['explanation'],
        "score": topic_relevancy['score'] * topic_continuity['score'] * topic_transition['score']
    }

def main():
    text = sys.argv[1]
    turn_number = sys.argv[2]
    previous_comments = sys.argv[3]
    comments = []
    try:
        loaded_comments = json.loads(previous_comments)
        if isinstance(loaded_comments, list):
            comments.extend(loaded_comments)
        else:
            print("Expected topics to be a list")
            sys.exit(2)
    except json.JSONDecodeError:
        print("Invalid JSON data")
        sys.exit(2)
    
    results = get_cohesion(text, turn_number, comments)
    print(json.dumps(results))
    sys.stdout.flush()

if __name__ == "__main__":
    main()