# import pandas as pd
import re
import json
import sys


##Put relevant training data into dataframe
##For example: df = pd.read_pickle("/path/to/pickle/file")
##             training_data_df = df
##Uses apply function to annotate the dataset
##For example: training_data_df['sentence_types'] = training_data_df['content'].apply(sentenceTypeClassifier)

##Counts the number of sentence within a string
##Input: String
def countSentences(text):
    # Split the text based on sentence-ending punctuation
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)

    # Filter out any empty strings resulting from the split
    sentences = [s.strip() for s in sentences if s.strip()]

    # Return the count of non-empty sentences
    return len(sentences)

##Description: Classification logic function for ML sentence type training data
##Input: String
##Takes in a sentence (String) as classifies it as being either exclamatory, interrogative, imperative, or declarative
##Output: String
def classifySentenceType(sentence):
    # Trim any leading/trailing whitespace
    sentence = sentence.strip()

    # Check for exclamatory sentence (ends with '!')
    if sentence.endswith('!'):
        return "exclamatory"

    # Check for interrogative sentence (ends with '?')
    elif sentence.endswith('?'):
        return "interrogative"

    # Check for imperative sentence
    # Imperative sentences often start with a verb and do not have a subject
    elif re.match(r"^(Please |Do |Don't |Let |Go |Take |Give |Bring |Tell |Show |Call |Stop |Listen |Come |Look |Wait |Help |Remember |Forget |Keep |Start |Finish )", sentence):
        return "imperative"

    # If none of the above, it is likely a declarative sentence
    else:
        return "declarative"

##Description: Classification wrapper function for ML sentence type training data
##Input: String
##Takes in a chunk of text and splits it into sentences
##Calls classifySentenceType on each sentence and determines the sentence type
##Output: List (String)
def sentenceTypeClassifier(text):
    # Split the text into individual sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)

    # Filter out any empty strings resulting from the split
    sentences = [s.strip() for s in sentences if s.strip()]

    # Classify each sentence and store the results in a list
    sentence_types = [classifySentenceType(sentence) for sentence in sentences]

    return sentence_types

##Description: Classification logic function for ML sentence form training data
##Input: String
##Takes in a sentence (String) as classifies it as being either simple, complex, compound, or compound-complex
##Output: String
def classifySentenceForm(sentence):

    # Lists of common coordinating and subordinating conjunctions - not finite
    coordinating_conjunctions = {"for", "and", "nor", "but", "or", "yet", "so"}
    subordinating_conjunctions = {"because", "since", "as", "although", "though", "while", "if", "unless", "until", "provided", "assuming", "even though", "in case"}

    # Split the sentence into words
    words = sentence.lower().split()

    # Flags for detecting conjunctions
    has_coordinating_conjunction = any(cc in words for cc in coordinating_conjunctions)
    has_subordinating_conjunction = any(sc in words for sc in subordinating_conjunctions)

    # Basic classification based on the presence of conjunctions
    if has_coordinating_conjunction and has_subordinating_conjunction:
        return "compound-complex"
    elif has_coordinating_conjunction:
        return "compound"
    elif has_subordinating_conjunction:
        return "complex"
    else:
        return "simple"

##Description: Classification wrapper function for ML sentence form training data
##Input: String
##Takes in a chunk of text and splits it into sentences
##Calls classifySentenceForm on each sentence and determines the sentence form
##Output: List (String)
def sentenceFormClassifier(text):
    # Split the text into individual sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)

    # Filter out any empty strings resulting from the split
    sentences = [s.strip() for s in sentences if s.strip()]

    # Classify each sentence and store the results in a list
    sentence_forms = [classifySentenceForm(sentence) for sentence in sentences]

    return sentence_forms

def main():
    transcript = sys.argv[1] 
    try:
        array = json.loads(transcript)
    except json.JSONDecodeError:
        print("Invalid JSON data")
        sys.exit(2)

    classified_sentences = []
    for i in range(len(array)):
        classified_sentences.append({ 
        "text": array[i], 
        "sentence_types": sentenceTypeClassifier(array[i]), 
        "sentence_forms": sentenceFormClassifier(array[i])
    })

    print(json.dumps(classified_sentences))
    sys.stdout.flush()

if __name__ == "__main__":
    main()