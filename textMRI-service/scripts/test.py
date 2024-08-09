import json
import sys

def main():
    transcript = sys.argv[1] 
    
    result = {
        "name": "Analyzed Transcript",
        "length": len(transcript),
        "word_count": len(transcript.split())
    }

    print(json.dumps(result))
    sys.stdout.flush()

if __name__ == "__main__":
    main()
