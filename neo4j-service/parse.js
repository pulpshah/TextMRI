import fs from "fs";
import { parse } from "csv-parse/sync";
// import axios from "axios";

const API_URL = "http://localhost:4000/";

// Function to create a GraphQL mutation
function createMutation(data) {
    return `
    mutation {
      createDocument(
        input: {
          turn: ${data.turn_number}
          speaker: "${data.speaker}"
          content: "${data.content.replace(/"/g, '\\"')}"
          role: "${data.role}"
        }
      ) {
        id
      }
      
      createText(
        input: {
          name: "${data.speaker}_${data.turn_number}"
          id: ${data.turn_number}
        }
      ) {
        id
      }
      
      addDocumentDocument(
        from: { name: "${data.speaker}_${data.turn_number}" }
        to: { turn: ${data.turn_number}, speaker: "${data.speaker}" }
      ) {
        from { id }
        to { id }
      }
      
      createTopic(
        input: {
          name: "${data.topics.replace(/"/g, '\\"')}"
        }
      ) {
        id
      }
      
      addMustContainTopic(
        from: { turn: ${data.turn_number}, speaker: "${data.speaker}" }
        to: { name: "${data.topics.replace(/"/g, '\\"')}" }
      ) {
        from { id }
        to { id }
      }
    }
  `;
}

// Function to send mutation to GraphQL API
async function sendMutation(mutation) {
    try {
        const response = await axios.post(API_URL, {
            query: mutation,
        });
        console.log("Mutation successful:", response.data);
    } catch (error) {
        console.error("Error sending mutation:", error.message);
    }
}

// // Read CSV and process each row
// fs.createReadStream('June 27, 2024 Presidential Debate Transcript.csv')
//   .pipe(csv())
//   .on('data', (row) => {
//     const mutation = createMutation(row);
//     // sendMutation(mutation);
//   })
//   .on('end', () => {
//     console.log('CSV file successfully processed');
//   });
const inputPath = "June 27, 2024 Presidential Debate Transcript.csv";

fs.readFile(inputPath, function (err, fileData) {
    const records = parse(fileData, {
        columns: true,
        skip_empty_lines: true,
    });

    for(let i = 0; i < records.length; i++) {
        const mutation = createMutation(records[i]);
        sendMutation(mutation);
    }
    // console.log(records.length)
    // console.log(records[0])
    // fs.writeFile('text.txt', JSON.stringify(records), (err) => {
    //     if (err) {
    //       console.error('Error writing to file:', err);
    //     } else {
    //       console.log('File written successfully');
    //     }
    //   });
});

/**
 * {
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
 */