import json
import pandas as pd
from openai import OpenAI
import os


# Initialize the OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

assistant = """

        You are an AI Comment Analysis Expert. Given a comment, the previous two comments, a bucket of topics, your job is to extract claims, biases, fallacies, 
        and compute the strength of multiple attributes of a comment. 

        If there is no previous comment or no comment before the previous comment, then it is the first or second comment in a conversation thread. 

        A bucket of topic is a list of topics that have been discussed in the conversation thread before this comment. For any attribute related to topic (claim_of_value_topic, topics, etc...), you are to search through 
        this list first and if any topics match the content and the specific attribute, you are to select it for that attribute. If not, extract a unique topic.

        For example, if my topic bucket includes "Medicaid" and the claim of fact is about expanding medicaid, then "medicaid" should be included in claim_of_facts_topic. 

        You are not exclusivly limited to the topic bucket. 

        An argument is an extension of a claim. It is the claim plus the because/reasoning for the claim.
        Claims of policies are defined as policies with that rhetorically have 'shoulds' and 'oughts'. 

        For any impacted_groups attributes, select groups of people or real-world entities/organizations. For example, you can include congress if related to passing legislation or Greenpeace if related to climate change. 

        For bias types, choose out of the following: "Overconfidence Bias", "Negativity Bias", "Sunk Cost Fallacy", "Status Quo Bias", "Self-Serving Bias", "Hindsight Bias", "Bandwagon Effect", "Availability Heuristic", "Anchoring Bias", "Confirmation Bias"
        For fallacy types, choose out of the following: "Begging the Question", "Equivocation", "False Cause", "Red Herring", "Circular Reasoning", "Hasty Generalization", "Slippery Slope", "False Dichotomoy", "Straw Man", "Ad Hominem"

        All epl_ethos, epl_logos, epl_pathos category scores are probabilistic such that it measures the likelihood the content has appealed to any of the categories.

        System 1 is characterized as fast, automatic, unconsious, and emotional response to situations and stimuli.
        System 2 is slow, effortful, and logical mode in which our brains operate when solving more complicated problems.
        system1_score and system2_score is a probabilistic score for each mode of thought where the sum of system1_score and system2_score must be 1. 

        Clarity is the probabilistic score that assess the likelihood that the comment is clear and comprehensible. 
        Relevancy is measures how relevant the comment is to the previous two comments. A high relevancy score means the comment is directly responding to the previous comment(s) 
        and a low score means the comment has little to nothing to do with the previous comment(s).

        All floats should be in the range of [0.0, 1.0). 

        Your results should be returned in a RFC-8259 compliant JSON of the following schema.: 

        {
            "claim_of_facts_abstractive_claim": "string",
            "claim_of_facts_extractive_supporting_quotes_claim": ["string"],
            "claim_of_facts_abstractive_argument": "string",
            "claim_of_facts_extractive_supporting_quotes_argument": ["string"],
            "claim_of_facts_topic": "string",
            "claim_of_facts_impacted_groups_populations": ["string"],

            "claim_of_value_abstractive_claim": "string",
            "claim_of_value_extractive_supporting_quotes_claim": ["string"],
            "claim_of_value_abstractive_argument": "string",
            "claim_of_value_extractive_supporting_quotes_argument": ["string"],
            "claim_of_value_topic": "string",
            "claim_of_value_impacted_groups_populations": ["string"],

            "claim_of_policy_abstractive_claim": "string",
            "claim_of_policy_extractive_supporting_quotes_claim": ["string"],
            "claim_of_policy_abstractive_argument": "string",
            "claim_of_policy_extractive_supporting_quotes_argument": ["string"],
            "claim_of_policy_topics": ["string"],
            "claim_of_policy_impacted_groups_populations": ["string"],

            "epl_ethos_trust": "float",
            "epl_ethos_power": "float",
            "epl_ethos_authority": "float",
            "epl_ethos_credibility": "float",

            "epl_pathos_anticipation": "float",
            "epl_pathos_joy": "float",
            "epl_pathos_trust": "float",
            "epl_pathos_fear": "float",
            "epl_pathos_surprise": "float",
            "epl_pathos_sadness": "float",
            "epl_pathos_disgust": "float",
            "epl_pathos_anger": "float",
            "epl_pathos_irony": "float",
            "epl_pathos_exaggeration": "float",
            "epl_pathos_pride": "float",
            "epl_pathos_bitterness": "float",
            "epl_pathos_resentment": "float",
            "epl_pathos_pity": "float",
            "epl_pathos_shame": "float",
            "epl_pathos_nostalgia": "float",
            "epl_pathos_awe": "float",
            "epl_pathos_remorse": "float",
            "epl_pathos_gratitude": "float",
            "epl_pathos_compassion": "float",

            "epl_logos_premise_strength": "float",
            "epl_logos_conclusion_strength": "float",
            "epl_logos_link_premise_conclusion_strength": "float",
            "epl_logos_bias_types": ["string"],
            "epl_logos_bias_text": ["string"],

            "epl_logos_fallacy_types": ["string"],
            "epl_logos_fallacy_text": ["string"],

            "clarity": "float",
            "clarity_expl": "String",

            "topics": ["string"],

            "relevancy": "float",
            "relevancy_expl": "String",

            "system1_score": "float",
            "system1_explanation": "String",
            "system2_score": "float",
            "system2_explanation": "String"
        }

    """
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
    
output_dir = "annotated_transcripts_pkl"
os.makedirs(output_dir, exist_ok=True)

# Process each JSON file in the transcript_json folder
input_dir = "transcripts_json"

for file_name in os.listdir(input_dir):
    if file_name.endswith('.json'):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name.replace('.json', '.pkl'))

        # Skip processing if the .pkl file already exists
        if os.path.exists(output_path):
            print(f"Skipping {file_name} as {os.path.basename(output_path)} already exists.")
            continue

        with open(input_path, 'r', encoding='utf-8') as file:
            input_data = json.load(file)

        # Process each turn
        processed_turns = []
        turn_number = 0

        previous_comment = ""
        previous_previous_comment = ""
        topic_bucket = ""

        for turn in input_data:
            turn_number += 1

            prompt = f"""
                Comment: {turn['content']},
                "Previous Comment": {previous_comment},
                "Comment before the Previous Comment": {previous_previous_comment},
                "Topic Bucket": {topic_bucket}
            """
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": assistant},
                    {"role": "user", "content": prompt},
                ]
            )

            previous_previous_comment = previous_comment
            previous_comment = turn['content']

            result = response.choices[0].message.content

            try:
                result = handle_response(result)
            except ValueError as e:
                print(f"File {file_name}, Turn Number {turn_number}: {e}")
                continue

            # Combine the original turn data with the extracted attributes
            combined_data = {**turn, **result}
            processed_turns.append(combined_data)

        # Create a dataframe from the processed turns
        df = pd.DataFrame(processed_turns)

        df.to_pickle(output_path)

