import json
import spacy 
import re
import sys
import os


rhetorical_Weight = []

nlp = spacy.load('en_core_web_sm')
#The wordWeight() function calculates the total number of words in each turn until it reads the entire data set.
def charWeight(text):
    charsum = {}
    for turn, content in text.items():
        # Count the number of characters in the content
        characters = len(content)
        
        # Assign the character count to the corresponding turn
        charsum[turn] = characters
    
    return charsum

#The wordWeight() function calculates the total number of words in each turn until it reads the entire data set.
def WordWeight(text):
    wordsum={}
    for turn, content in text.items():
        # Split the content into words using regex to handle different delimiters
        words = re.split(r'\W+', content)
        
        # Filter out any empty strings that might be in the list due to splitting
        words = [word for word in words if word]

        wordsum[turn] = len(words)
    return wordsum

#The sentWeight() function calculates the total number of sentences in each turn until it reads the entire data set.
def sentWeight(text):
    sentsum={}
    for turn, content in text.items():
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', content)
        # Filter out any empty strings resulting from the split
        sentences = [s.strip() for s in sentences if s.strip()]
        sentsum[turn] = len(sentences)

    return sentsum

#The namedentWeight() function calculates the total number of named entities in each turn until it reads the entire data set.
def namedentWeight(text):
    namedentsum = {}
    for turn, content in text.items():
        try:
            # Process the text with spaCy to get named entities
            doc = nlp(content)
            # Count the number of named entities
            namedsum = len(doc.ents)
            # Store the count in the dictionary with turn as the key
            namedentsum[turn] = namedsum
        except Exception as e:
            # Handle any unexpected errors
            print(f"Error processing turn {turn}: {e}")
            namedentsum[turn] = 0  # Assign a default value or handle the error as needed
    return namedentsum

def rhetoricalWeight(textTable):
    charsum = charWeight(textTable)
    wordsum = WordWeight(textTable)
    sentsum = sentWeight(textTable)
    namedentsum = namedentWeight(textTable)
    rhetorical_weights = []
    for turn in textTable:
        turn_weight = charsum[turn] + wordsum[turn] + sentsum[turn] + namedentsum[turn]
        rhetorical_weights.append(turn_weight)
    return rhetorical_weights, sentsum, wordsum, charsum, namedentsum

#takes in json transcript with turn number and content and returns an array of rhetorical weight
def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        sys.exit(1)
    
    # file_path = sys.argv[1]
    data = sys.argv[1]
    # if not os.path.isfile(file_path):
    #     print(f"{file_path} is not a valid file.")
    #     sys.exit(2)
    
    try:
        # Open the file with UTF-8 encoding
        # with open(file_path, 'r', encoding='utf-8') as file:
        #     transcript = json.load(file)
        transcript = json.loads(data)
        
        hashtable = {item['turn_number']: item['content'] for item in transcript}
        rhetorical_weights = rhetoricalWeight(hashtable)
        # list composed of [rhetorical weight],{turn:charsum}, {turn:wordsum}, {turn:sentsum}, {turn:namedentsum} 
        weights = []
        for i in range(len(rhetorical_weights[0])):
                turn = i+1
                weights.append({
                    "rhetorical_weight":rhetorical_weights[0][i],   
                    "sentence_weight":rhetorical_weights[1].get(turn, 0), 
                    "word_weight":rhetorical_weights[2].get(turn, 0),  
                    "character_weight":rhetorical_weights[3].get(turn, 0),   
                    "namedent_weight":rhetorical_weights[4].get(turn, 0)             
                
                })
        print(json.dumps(weights))
        return weights
    except json.JSONDecodeError:
        print("Invalid JSON string.")
        sys.exit(2)
    except Exception as e:
        print(f"Error processing JSON string: {e}")
        sys.exit(2)
    # except json.JSONDecodeError:
    #     print(f"Invalid JSON data in {file_path}")
    #     sys.exit(2)
    # except UnicodeDecodeError:
    #     print(f"Error decoding the file {file_path}. Ensure it is encoded in UTF-8.")
    #     sys.exit(2)
    # except Exception as e:
    #     print(f"Error processing {file_path}: {e}")
    #     sys.exit(2)

if __name__ == "__main__":
    main()