# TextMRI

## Getting started locally

1. Clone the repository on to your local computer
2. run ```cd``` in the terminal to go into the repository 
3. run ```npm install``` in the terminal to install all the node modules
4. run ```npm run dev``` to get the server running on your local host
5. follow the link in the terminal to go to the graphql studio

## Example Query

## Example Mutation

```graphql
{
  "input": [
    {
      "name": "Test Transcript",
      "hasTextText": {
        "create": {
          "node": {
            "name": "Text Transcript Text"
          }
        }
      },
      "containsActorActor": {
        "create": [
          {
            "node": {
              "name": "Text Actor #1",
              "role": "Actor",
              "spokeInTurn": {
                "create": [
                  {
                    "node": {
                      "turn_number": 1,
                      "content": "WOW!",
                      "talkedAboutTopic": {
                        "create": [
                          {
                            "node": {
                              "name": "TOPIC!"
                            }
                          }
                        ]
                      }
                    }
                  },
                  {
                    "node": {
                      "turn_number": 2,
                      "content": "W!"
                    }
                  }
                ]
              }
            }
          },
          {
            "node": {
              "name": "Actor #2",
              "role": "Actress"
            }
          }
        ]
      }
    }
  ]
}
```