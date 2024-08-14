from openai import OpenAI
import json
import pandas as pd

client = OpenAI(api_key="YOUR-API-KEY")

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
    
##Description: Clause extraction and identification for ML sentence form training data
##Input: DataFrame
##Uses OpenAI to extract the clauses from sentences stored in a DataFrame cell into independent and dependent clauses.
##Identifies each clause and provides an explanation
##Output: List (Dict)

##Use pd.json_normalize when trying to convert the returned list to a DataFrame


def extractClauses(df):

    independent_clause_rules = [
    "A clause that can stand alone as a complete sentence.",
    "A clause that contains a subject and a predicate (verb).",
    "A clause that expresses a complete thought.",
    "A clause that is not introduced by a subordinating conjunction (e.g., 'although', 'because', 'since').",
    "A clause that does not begin with a relative pronoun (e.g., 'who', 'which', 'that') unless it functions as the subject.",
    "A clause that does not start with a dependent marker word (e.g., 'if', 'when', 'while', 'since', 'although').",
    "A clause that may start with an independent marker word (e.g., 'however', 'therefore', 'moreover').",
    "A clause that may be connected to another independent clause by a coordinating conjunction (e.g., 'and', 'but', 'or', 'nor', 'for', 'so', 'yet').",
    "A clause that is not interrupted by a non-essential phrase or clause, unless correctly punctuated with commas."
    ]


    dependent_clause_rules = [
    "A clause that cannot stand alone as a complete sentence.",
    "A clause that contains a subject and a predicate (verb) but does not express a complete thought.",
    "A clause that is introduced by a subordinating conjunction (e.g., 'although', 'because', 'since').",
    "A clause that begins with a relative pronoun (e.g., 'who', 'which', 'that') and provides additional information about a noun.",
    "A clause that starts with a dependent marker word (e.g., 'if', 'when', 'while', 'since', 'although').",
    "A clause that serves as an adjective, adverb, or noun within a sentence.",
    "A clause that is usually attached to an independent clause to form a complete sentence.",
    "A clause that may be punctuated with a comma when it precedes the independent clause in a sentence.",
    "A clause that often provides background information or clarifies the meaning of the independent clause."
    ]

    clauses = []
    #for row in df.itertuples():
    for idx, row in df.iterrows():
        system_prompt_epl_scores = """You are an AI Rhetorical Analysis Expert. Your job is to analyze a sentence and separate it into the independent and dependent clauses composing it. """ +\
                                   """For each clause, identify them as either "independent" or "dependent". """ +\
                                   f"""Identify independent clauses by the following rules: {independent_clause_rules}.  """ +\
                                   f"""Identify dependent clauses by the following rules: {dependent_clause_rules} """ +\
                                   """Provide exactly 1-2 sentence explainer (expl) for each classification. """ +\
                                   """Return a single RFC 8259 compliant JSON object:
                                      {"sentences": List (String)
                                      "clauses": List (String),
                                      "clause_types": List (String),
                                      "clause_expl": List (String)
                                      }"""
        user_content = "Analyze the turn: " + json.dumps(row.to_dict())
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt_epl_scores},
                {"role": "user", "content": user_content}
            ]
        )
        try:
            result = response.choices[0].message.content
            result = handle_response(result)

        except ValueError as e:
            print(e)

        clauses.append(result)

    return clauses