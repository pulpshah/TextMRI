import express from "express";
import { request, gql } from "graphql-request";
import bodyParser from "body-parser";
import { spawn } from "child_process";
import {
    createTextTranscriptNode,
    createTextNode,
    createActorNode,
    createTopicNode,
    createTurnNode,
    createDocumentNode,
} from "./utils/nodes/createNodes.js";
import {
    updateDocumentNodeWithTopics,
    updateTurnNodeWithTopics,
} from "./utils/nodes/updateNode.js";
import { extractUniqueSpeakers } from "./utils/extractUniqueSpeakers.js";
import { extractTopics } from "./utils/scripts/extractTopics.js";
import dotenv from "dotenv";
import axios from "axios";
// const { createRhetoricalNodes } = require('./parse');

dotenv.config();
const app = express();
app.use(express.json({ limit: "10mb" }));
app.use(bodyParser.json());

app.post("/transcript", async (req, res) => {
    const { transcript } = req.body;
    const data = {
        actors: {},
        topics: {},
    };

    if (!transcript) {
        return res.status(400).json({ error: "Transcript is required" });
    }

    try {
        const textTranscript = await createTextTranscriptNode(transcript.name);
        data.transcript = textTranscript[0];
        const text = await createTextNode(transcript.name, data.transcript.id);
        data.text = text[0];

        const speakers = extractUniqueSpeakers(transcript.debate);

        for (const speaker of speakers) {
            const actor = await createActorNode(
                speaker.name,
                speaker.role,
                data.transcript.id
            );
            data.actors[actor[0].name] = actor[0].id;
        }

        for (const turn of transcript.debate) {
            const turnNode = await createTurnNode(
                turn.turn_number,
                turn.content,
                data.transcript.id,
                data.actors[turn.speaker]
            );
            const documentNode = await createDocumentNode(
                turn.turn_number,
                turn.content,
                turn.speaker,
                turn.role,
                data.text.id
            );

            const result = await extractTopics(
                Object.keys(data.topics),
                turn.content
            );
            let extracted_topics = JSON.parse(result);
            extracted_topics = extracted_topics.topics;
            console.log(extracted_topics);
            for (const topic of extracted_topics) {
                if (!data.topics[topic]) {
                    const topicNode = await createTopicNode(
                        topic,
                        data.transcript.id
                    );
                    data.topics[topicNode[0].name] = topicNode[0].id;
                }
                await updateTurnNodeWithTopics(
                    data.topics[topic],
                    turnNode[0].id
                );
                await updateDocumentNodeWithTopics(
                    data.topics[topic],
                    documentNode[0].id
                );
            }
        }
        // const result = await extractSentenceData(JSON.stringify(transcript));

        res.status(200).send("Transcript processed successfully");
    } catch (error) {
        console.error("Error processing transcript:", error);
        res.status(500).json({ error: "Internal Server Error" + error });
    }
});

app.get("/test", async (req, res) => {
    try {
        const topics = [];
        const content =
            "This debate is being produced by CNN and it’s coming to you live on CNN, CNN International, CNN.com, CNN Max, and CNN Espanol. This is a pivotal moment between President Joe Biden and former President Donald Trump in their rematch for the nation’s highest office. Each will make his case to the American people with just over four months until Election Day. Good evening. I’m Dana Bash, anchor of CNN’s “Inside Politics” and co-anchor of “State Of The Union.";

        const result = await extractTopics(topics, content);
        const extracted_topics = JSON.parse(result);

        for (const topic of extracted_topics) {
            if (topics.includes(topic)) {
            }
        }
        res.status(200).json(JSON.parse(result));
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ error: "Internal Server Error: \n" + error });
    }
});

app.post("/texts", async (req, res) => {
    try {
        const weight = await extractWeights(req.body);
        // const clause = await extractClause(req.body)
        const parsedWeight = JSON.parse(weight);
        // const parsedClause = JSON.parse(clause);

        res.status(200).json(parsedWeight);
    } catch (error) {
        console.error("Error:", error);
        res.status(500).json({ error: "Internal Server Error" + error });
    }
});

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
