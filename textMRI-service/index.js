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
    createKnowledgeNode,
    createClarityNode,
    createHumorNode
} from "./utils/nodes/createNodes.js";
import {
    updateDocumentNodeWithTopics,
    updateTurnNodeWithTopics,
} from "./utils/nodes/updateNode.js";
import { extractUniqueSpeakers } from "./utils/extractUniqueSpeakers.js";
import { extractTopics } from "./utils/scripts/extractTopics.js";
import dotenv from "dotenv";
import { extractClarity, extractHumor, extractKnowledge } from "./utils/extractData.js";

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
        // Create the text transcript and text node
        const textTranscriptNode = await createTextTranscriptNode(transcript.name);
        data.transcript = textTranscriptNode[0];
        const textNode = await createTextNode(transcript.name, data.transcript.id);
        data.text = textNode[0];

        // Extract knowledge from the transcript and create a knowledge node
        let knowledge = await extractKnowledge(transcript.debate);
        knowledge = JSON.parse(knowledge);

        const knowledgeNode = await createKnowledgeNode(knowledge.type, knowledge.explanation, data.text.id);
        data.knowledge = knowledgeNode[0];  

        // Extract unique speakers from the transcript and create actor nodes
        const speakers = extractUniqueSpeakers(transcript.debate);
        for (const speaker of speakers) {
            const actor = await createActorNode(
                speaker.name,
                speaker.role,
                data.transcript.id
            );
            data.actors[actor[0].name] = actor[0].id;
        }

        // For each turn in the transcript, generate dynamic node sfor the turn
        for (const turn of transcript.debate) {
            // Create a turn node and document node
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

            // Update the turn and document nodes relationships with the topics
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

            // Create a clarity node and humor node
            let clarity = await extractClarity(turn.content);
            clarity = JSON.parse(clarity);
            const clarityNode = await createClarityNode(clarity, documentNode[0].id);

            let humor = await extractHumor(transcript.debate[0].content);
            humor = JSON.parse(humor);
            const humorNode = await createHumorNode(humor, documentNode[0].id);


            // Extract topics from the turn and create topic nodes
            const result = await extractTopics(
                Object.keys(data.topics),
                turn.content
            );
            let extracted_topics = JSON.parse(result);
            extracted_topics = extracted_topics.topics;
            console.log(extracted_topics);

            // TODO: Create a cohesion node based on the cohesion script
        }

        res.status(200).send("Transcript processed successfully");
    } catch (error) {
        console.error("Error processing transcript:", error);
        res.status(500).json({ error: "Internal Server Error" + error });
    }
});

app.post("/test", async (req, res) => {
    const { transcript } = req.body;
    if (!transcript) {
        return res.status(400).json({ error: "Transcript is required" });
    }
    try {
        const document_id = "414f0bed-d198-4403-a836-626259c68571"
        let humor = await extractHumor(transcript.debate[0].content);
        humor = JSON.parse(humor);
        console.log(humor)

        const humorNode = await createHumorNode(humor, document_id);
        console.log(humorNode)
        res.status(200).send("Test ran successfully");
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
