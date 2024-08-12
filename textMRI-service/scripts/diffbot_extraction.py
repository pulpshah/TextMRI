import requests
import pandas as pd
import pickle
import os
from bs4 import BeautifulSoup

diff_token = 'f17dc30195a2724fa3be6d59b5183ff9'
transcript_dir = 'TRANSCTIP_DIR'
output_dir = 'OUTPUT_DIR'

# Takes in a directory (string) from which files are to be read
# Loads all of the pickle files that are to be opened and processed by the script
# Returns all of the dataframes (dictionary of strings)
def load_pickle_files(directory):
    dataframes = {}
    for filename in os.listdir(directory):
        if filename.endswith('.pkl'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'rb') as file:
                df = pd.read_pickle(file)
                dataframes[filename] = df
    return dataframes

# Takes in a query (string)
# Searches Diffbot's Knowledge Graph based 
# on that query
# Returns the first result of the query (string) in the form of a URL
def query_knowledge_graph(query):
    diffbot_url = f'https://api.diffbot.com/v3/knowledgegraph?token={diff_token}&query={query}'
    
    response = requests.get(diffbot_url)
    response.raise_for_status()
    
    data = response.json()
    if 'objects' not in data:
        print("No results found.")
        return None
    
    results = data['objects']
    urls = [result.get('url') for result in results if 'url' in result]
    if urls:
        return urls
    return None

# Takes in all the URLs (list of strings) found by Diffbot, key words (string) and groups (strings) associated with a turn/row in a dataframe
# Iterates through all of the URLs and ensures that all of the strings in the specified columns actually appear in the web page of the URL
# Returns the validated references (list of strings)
def get_best_reference(refs, topics, groups, claims, args):
    better_refs = []
    for ref in refs:
        if len(better_refs) >= 3:
            break
        try:
            response = requests.get(ref)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                text = soup.get_text()
                
                topics_match = all(topic.lower() in text.lower() for topic in topics) 

                min_group_matches = int(0.9 * len(groups)) 
                group_matches = sum(group.lower() in text.lower() for group in groups)

                min_claim_matches = int(0.6 * len(claims))
                claim_matches = sum(claim.lower() in text.lower() for claim in claims)

                min_arg_matches = int(0.6 * len(args))
                arg_matches = sum(arg.lower() in text.lower() for arg in args)

                if (topics_match and group_matches >= min_group_matches) or (topics_match and group_matches >= min_group_matches and min_claim_matches <= claim_matches and min_arg_matches <= arg_matches):
                    better_refs.append(ref)
                    return better_refs
        except requests.RequestException as e:
            print(f"Error accessing {ref}: {e}")
    
    return None

# Takes in references (list of strings)
# Queries Diffbot for each reference to extract any possible image or video URLS
# Returns dictionary of corresponding images and videos
def get_media(refs):
    refs_img_vids = {}
    for ref in refs:
        diffbot_url = f'https://api.diffbot.com/v3/analyze?token={diff_token}&url={ref}'
        response = requests.get(diffbot_url)
        response.raise_for_status()
    
        data = response.json()
        if 'objects' not in data:
            print(f"No results found for {ref}.")
            continue
    
        results = data['objects']
        
        image_urls = []
        video_urls = []
                
        for result in results:
            if 'images' in result:
                for image in result['images']:
                    image_url = image.get('url')
                    if image_url:
                        image_urls.append(image_url)
            
            if 'videos' in result:
                for video in result['videos']:
                    video_url = video.get('url')
                    if video_url:
                        video_urls.append(video_url)
        
        if image_urls or video_urls:
            refs_img_vids[ref] = {
                'IMAGES': image_urls,
                'VIDEOS': video_urls
            }
        
    return refs_img_vids


# Takes in a list (of strings)
# Converts list (of strings) to a single comma-separated string
# Returns the new string
def list_to_string(lst):
    if isinstance(lst, list):
        return ', '.join(lst)
    return lst

# Takes in references (list of strings)
# For each reference, uses Diffbot's Analyze API to extract the type of content the webpage was in
# Returns the reference types (dictionary of strings)
def ref_type(refs):
    ref_types = {}
    for ref in refs:
        diffbot_url = f'https://api.diffbot.com/v3/analyze?token={diff_token}&url={ref}'
        response = requests.get(diffbot_url)
        response.raise_for_status()
    
        data = response.json()
        if 'objects' not in data:
            print(f"No results found for {ref}.")
            continue
    
        results = data['objects']
        ref_type = results[0].get('type').upper() if results else 'NO TYPE'
        if ref_type:
           ref_types[ref] = ref_type
    
    return ref_types

# Takes in a dataframe and number of rows (integer) to be processed in that dataframe
# Creates new topic_columns corresponding to the topic_columns to be looked at and queried in the dataframe
# Updates those topic_columns with extracted reference in the form of a URL, if found
# Returns an updated dataframe with the extracted references
def update_df(df, num_rows):
    df['claim_of_policy_topics'] = df['claim_of_policy_topics'].apply(list_to_string)

    df['facts_topic_ref'] = None
    df['value_topic_ref'] = None
    df['policy_topic_ref'] = None

    df_subset = df.head(num_rows)

    for index, row in df_subset.iterrows():
        for abs_claim_column, abs_arg_column, topic_column, group_column, ref_column in [
            ('claim_of_facts_abstractive_claim', 'claim_of_facts_abstractive_argument','claim_of_facts_topic', 'claim_of_facts_impacted_groups_populations', 'facts_topic_ref'),
            ('claim_of_value_abstractive_claim','claim_of_value_abstractive_argument','claim_of_value_topic', 'claim_of_value_impacted_groups_populations', 'value_topic_ref'),
            ('claim_of_policy_abstractive_claim','claim_of_policy_abstractive_argument','claim_of_policy_topics', 'claim_of_policy_impacted_groups_populations', 'policy_topic_ref')]:
            
            topic_text = row.get(topic_column)
            group_text = row.get(group_column, [])
            claim_text = row.get(abs_claim_column)
            arg_text = row.get(abs_arg_column)

            if topic_text and group_text:
                refs = query_knowledge_graph(topic_text)
                if refs:
                    topic_words = topic_text.split() if isinstance(topic_text, str) else []
                    group_words = ' '.join(group_text) if isinstance(group_text, list) else ''
                    claim_words = claim_text.split() if isinstance(claim_text, str) else []
                    arg_words = arg_text.split() if isinstance(arg_text, str) else []

                    best_refs = get_best_reference(refs, topic_words, group_words.split(), claim_words, arg_words)
                    if best_refs:
                        best_ref_types = ref_type(best_refs)
                        best_ref_media = get_media(best_refs)
                        df.at[index, ref_column] = [(best_ref_types.get(ref), ref, best_ref_media.get(ref)) for ref in best_refs]

    return df

# Transfers all of the updated dataframes to the noted output directory
for filename, df in load_pickle_files(transcript_dir).items():
    updated_df = update_df(df, num_rows=5)
    output_filepath = os.path.join(output_dir, filename)
    with open(output_filepath, 'wb') as file:
        pickle.dump(updated_df, file)