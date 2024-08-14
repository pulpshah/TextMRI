import pandas as pd

df = pd.read_pickle("info.pkl")

import dtale

def open_dataframe_in_dtale(df):

    d = dtale.show(df)
    d.open_browser()

open_dataframe_in_dtale(df)

from openai import OpenAI
import os

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = api_key)

def trim_df(df, columns):
    
    # Ensure the columns_to_remove is a list
    if not isinstance(columns, list):
        raise ValueError("columns_to_remove must be a list")
    
    # Remove the specified columns
    df_modified = df.drop(columns=columns, errors='ignore')
    
    return df_modified

import json

def df_to_string(df):
    dict = df.to_dict()
    str = json.dumps(dict)

    return str

#Plan
def metacognition1(df):

    ignore = [

        "epl_pathos_anticipation",
        "epl_pathos_joy",
        "epl_pathos_trust",
        "epl_pathos_fear",
        "epl_pathos_surprise",
        "epl_pathos_sadness",
        "epl_pathos_disgust",
        "epl_pathos_anger",
        "epl_pathos_irony",
        "epl_pathos_exaggeration",
        "epl_pathos_pride",
        "epl_pathos_bitterness",
        "epl_pathos_resentment",
        "epl_pathos_pity",
        "epl_pathos_shame",
        "epl_pathos_nostalgia",
        "epl_pathos_awe",
        "epl_pathos_remorse",
        "epl_pathos_gratitude",
        "epl_pathos_compassion",
    ]

    df = trim_df(df, ignore)

    assistant = """ 

    You are an AI metacognition expert. Given a debate transcript where each turn is annotated with claims of facts, 
    claims of value, claim of policy, ethos, pathos, logos, clarity, and topics, answer the following in 1-2 paragraphs:

    How do each participant (Joe Biden, Donald Trump, Jake Tapper, Dana Bash) plan their claims and arguments for each mostly 
    discussed topic? What strategies do they used based on the annotation. Provide examples with direct quotes from the 
    transcript to support your response.  

    """

    prompt = f""" 

    Transcript: {df}
    
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    return result
    
#Monitor
def metacognition2(df):
    assistant = """ 

    You are an AI metacognition expert. Given a debate transcript where each turn is annotated with claims of facts, 
    claims of value, claim of policy, ethos, pathos, logos, clarity, and topics, answer the following in 1-2 paragraphs:

    How do each participant (Joe Biden, Donald Trump, Jake Tapper, Dana Bash) monitor the effectivness of their arguments and 
    rhetorical strategies (ethos, pathos, logos) during the debate? What adjustments do they make if a particular strategy isn't working?
    Provide examples with direct quotes from the transcript to support your response.
    

    """

    prompt = f""" 

    Transcript: {df}
    
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    return result

#Evaluate
def metacognition3(df):
    assistant = """

    You are an AI metacognition expert. Given a debate transcript where each turn is annotated with claims of facts, 
    claims of value, claim of policy, ethos, pathos, logos, clarity, and topics, answer the following in 1-2 paragraphs:

    How do the participants (Joe Biden, Donald Trump, Jake Tapper, Dana Bash) evaluate the success of their arguments and 
    strategies after presenting them? Provide examples with direct quotes from the transcript to support your response.

    """

    prompt = f""" 

    Transcript: {df}
    
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    return result

#Reflection on plan, monitor, evaluate thinking
def metacognition4(df, analysis):
    assistant = """ 

    You are an AI metacognition expert. Given a debate transcript where each turn is annotated with claims of facts, 
    claims of value, claim of policy, ethos, pathos, logos, clarity, and topics as well as an analysis of each participant's planning, monitoring, 
    and evaluation, answer the following in 1 paragraph:

    How do the participants' (Joe Biden, Donald Trump, Jake Tapper, Dana Bash) metacognitive practices contribute to their overall performance in 
    the debate? 

    """


    prompt = f""" 

    Transcript: {df}
    Analysis of Planning, Monitoring, Evaluation: {analysis}
    
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    return result

#System1 Thinking
def system1(df):
    assistant = """ 

    You are an AI metacognition expert. Given a debate transcript where each turn is annotated with claims of facts, 
    claims of value, claim of policy, ethos, pathos, logos, clarity, and topics, answer the following in 1 paragraphs:
    
    Identify instances where participants rely on fast, automatic, and intuitive responses. How do emotional appeals (pathos) and instinctive 
    rhetorical strategies (ethos) reflect System 1 thinking? Provide examples from the transcript annotations where participants use automatic 
    thinking to make quick judgments or decisions.

    """

    prompt = f""" 

    Transcript: {df}
    
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    return result

#System2 Thinking
def system2(df):
    assistant = """ 

    You are an AI metacognition expert. Given a debate transcript where each turn is annotated with claims of facts, 
    claims of value, claim of policy, ethos, pathos, logos, clarity, and topics, answer the following in 1 paragraphs:

    Highlight moments where participants engage in slow, effortful, and logical reasoning. How do they analyze complex problems and construct 
    detailed arguments? Discuss how participants evaluate the strength of their premises and conclusions (logos) and adjust their strategies 
    based on logical analysis. Provide examples from the transcript annotations where participants demonstrate deliberate, analytical thinking.



    """

    prompt = f""" 

    Transcript: {df}
    
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    return result

#Reflection on system thinking
def system3(df, analysis):
    assistant = """ 

    You are an AI metacognition expert. Given a debate transcript where each turn is annotated with claims of facts, 
    claims of value, claim of policy, ethos, pathos, logos, clarity, and topics as well as reflection on System 1 
    and System 2 thinking, answer the following in 1 paragraph:

    Analyze how the participants switch between System 1 and System 2 thinking throughout the debate. For each participant, what 
    triggers these switches? Discuss any biases or fallacies identified in the annotations and how they relate to the participants' 
    use of System 1 or System 2 thinking.

    """

    prompt = f""" 

    Transcript: {df}, 
    Analysis of System 1 and System 2: {analysis}
    
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": assistant},
            {"role": "user", "content": prompt},
        ]
    )

    result = response.choices[0].message.content
    return result

def write_responses_to_file(responses, file_path):
    
    with open(file_path, 'a') as file:
        for response in responses:
            file.write(response + "\n\n")  # Add newlines for readability

metacognition = []
metacognition.append(metacognition1(df))
metacognition.append(metacognition2(df))
metacognition.append(metacognition3(df))


analysis1 = " ".join(metacognition)
reflection1 = metacognition4(df, analysis1)

system = []
system.append(system1(df))
system.append(system2(df))

analysis2 = " ".join(system)
reflection2 = system3(df, analysis2)

responses = []
responses.extend(metacognition)
responses.append(reflection1)
responses.extend(system)
responses.append(reflection1)

write_responses_to_file(responses, 'responses.txt')
