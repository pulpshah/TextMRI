import fs from "fs";
import { parse } from "csv-parse/sync";
import axios from "axios";

const API_URL = "http://localhost:4000/";

const data = {
    actors: {},
    topics: {},
};

function parseArray(array) {
    array = array.slice(1, -1);
    let arr = array.split(", ");
    return arr.map((item) => item.slice(1, -1));
}

async function createTextTranscriptNode(name) {
    const mutation = `
    mutation {
      createTextTranscripts(
        input: {
          name: "${name}"
        }
      ) {
        textTranscripts {
          id,
          name
        }
      }
    }

  `;
    try {
        const response = await axios.post(API_URL, {
            query: mutation,
        });
        data.transcript =
            response.data.data.createTextTranscripts.textTranscripts[0].id;
    } catch (error) {
        console.error("Error sending mutation:", error.message);
    }
}

async function createActorNode({ name, role }) {
    console.log(`Creating actor: ${name}`);
    const mutation = `
    mutation {
        createActors(
            input: {
                name: "${name}",
                role: "${role}",
                texttranscriptMustContain: {
                connect: {
                    where: {
                    node: {
                        id: "${data.transcript}"
                    }
                    }
                }
                }
            }
            ) {
            actors {
                id,
                name,
                role
            }
        }
    }

`;
    try {
        const response = await axios.post(API_URL, {
            query: mutation,
        });
        const actor = response.data.data.createActors.actors[0];
        data[actor.name] = actor.id;
        console.log(`Created actor: ${actor.name}`);
    } catch (error) {
        console.error("Error creating actor mutation:", error.message);
    }
}

async function createTopicNode({ name }) {
    const mutation = `
        mutation {
        createTopics(
            input: {
            name: "${name}",
            texttranscriptMustContain: {
                connect: {
                where: {
                    node: {
                    id: "${data.transcript}"
                    }
                }
                }
            }
            }
        ) {
            topics {
                id,
                name
            }
        }
    }

`;
    try {
        const response = await axios.post(API_URL, {
            query: mutation,
        });
        const topic = response.data.data.createTopics.topics[0];
        data.topics[topic.name] = topic.id;
        console.log(`Created topic: ${topic.name}`);
    } catch (error) {
        console.error("Error creating topic mutation:", error.message);
    }
}

async function createTurnNode(info) {
    const { speaker, role, turn_number, content, topics } = info;
    const parsedTopics = parseArray(topics);
    if (!data.actors[speaker]) {
        await createActorNode({ name: speaker, role });
    }
    for (let topic of parsedTopics) {
        if (!data.topics[topic]) {
            await createTopicNode({ name: topic });
        }
    }
    const mutation = `
        mutation {
            createTurns(
            input: {
                turn_number: ${turn_number},
                content: "${content}",
                texttranscriptMustContain: {
                connect: {
                    where: {
                    node: {
                        id: "${data.transcript}"
                    }
                    }
                }
                }
                talkedAboutTopic: {
                connect: {
                    where: {
                    node: {
                        id: "${data.topics[parsedTopics[0]]}"
                    }
                    }
                }
                }
                actorSpokeIn: {
                connect: {
                    where: {
                    node: {
                        id: "6b30fb1c-095a-4ef1-b8d1-8ed3b39f50a2"
                    }
                    }
                }
                }
            }
            ){
            turns {
                id,
                turn_number,
                content
            }
        }
    }
  
  `;

    let turn_id;
    try {
        const response = await axios.post(API_URL, {
            query: mutation,
        });
        turn_id = response.data.data.createTurns.turns[0].id;
        console.log(`Created turn: ${turn_id}`);
    } catch (error) {
        console.error("Error sending turn mutation:", error.message);
    }

    if (parsedTopics.length > 1) {
        for (let i = 1; i < parsedTopics.length; i++) {
            const updateMutation = `
                mutation {
                    updateTurns(
                        connect: {
                            talkedAboutTopic: {
                                where: {
                                    node: {
                                        id: "${data.topics[parsedTopics[i]]}"
                                    }
                                }
                            }
                        },
                        where: { id: "${turn_id}"}
                    ) {
                        turns {
                            id
                            turn_number
                            content
                        }
                    }
                }
            `;
            try {
                await axios.post(API_URL, {
                    query: updateMutation,
                });
            } catch (error) {
                console.error("Error sending mutation:", error.message);
            }
        }
    }
}

const inputPath =
    "neo4j-service/June 27, 2024 Presidential Debate Transcript.csv";

async function createPIO() {
    await createTextTranscriptNode(
        "June 27, 2024 Presidential Debate Transcript"
    );

    fs.readFile(inputPath, function (err, fileData) {
        const records = parse(fileData, {
            columns: true,
            skip_empty_lines: true,
        });

        for(let i = 0; i < records.length; i++) {
            createTurnNode(records[i]);
        }
    });
}

createPIO();

// fs.readFile(inputPath, function (err, fileData) {
//     const records = parse(fileData, {
//         columns: true,
//         skip_empty_lines: true,
//     });

//     for(let i = 0; i < records.length; i++) {
//         const mutation = createMutation(records[i]);
//         // sendMutation(mutation);
//     }
//     console.log(records[0])
//     // console.log(records[0])
//     fs.writeFile('text.json', JSON.stringify(records), (err) => {
//         if (err) {
//           console.error('Error writing to file:', err);
//         } else {
//           console.log('File written successfully');
//         }
//       });
// });
