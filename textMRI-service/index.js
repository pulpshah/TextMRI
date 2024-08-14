import express from 'express';
import { request, gql } from 'graphql-request';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';
import { createTextTranscriptNode, createTextNode, createActorNode, createTopicNode, createTurnNode, createDocumentNode } from './utils/nodes/createNodes.js';
import { updateDocumentNodeWithTopics, updateTurnNodeWithTopics } from './utils/nodes/updateNode.js';
import { extractUniqueSpeakers } from './utils/extractUniqueSpeakers.js';
import { extractTopics } from './utils/scripts/extractTopics.js';
import dotenv from "dotenv";
// const { createRhetoricalNodes } = require('./parse');

dotenv.config();
const app = express();
app.use(bodyParser.json());

app.post('/transcript', async (req, res) => {
    const { transcript } = req.body;
    const data = {
        actors: {},
        topics: {},
    };

    if (!transcript) {
        return res.status(400).json({ error: 'Transcript is required' });
    }

    try {
        const textTranscript = await createTextTranscriptNode(transcript.name);
        data.transcript = textTranscript[0];
        const text = await createTextNode(transcript.name, data.transcript.id);
        data.text = text[0]

        const speakers = extractUniqueSpeakers(transcript.debate);

        for (const speaker of speakers) {
            const actor = await createActorNode(speaker.name, speaker.role, data.transcript.id);
            data.actors[actor[0].name] = actor[0].id;
        }

        console.log(data)
        for( const turn of transcript.debate){
            const turnNode = await createTurnNode(turn.turn_number, turn.content, data.transcript.id, data.actors[turn.speaker].id);
            const documentNode = await createDocumentNode(turn.turn_number, turn.content, turn.speaker, turn.role, data.text.id);

            const result = await extractTopics(topics, turn.content);
            const extracted_topics = JSON.parse(result)
            for(const topic of extracted_topics){
                if(data.topics[topic]){
                    
                } else {
                    const topicNode = await createTopicNode(topic, data.transcript.id);
                    
                    await updateTurnNodeWithTopics(turnNode[0].id, topicNode[0].id);
                    await updateDocumentNodeWithTopics(documentNode[0].id, topicNode[0].id);

                }
            }

        }
        // const result = await extractSentenceData(JSON.stringify(transcript));

        res.status(200).send('Transcript processed successfully');
    } catch (error) {
        console.error('Error processing transcript:', error);
        res.status(500).json({ error: 'Internal Server Error' + error });
    }
});

app.get('/transcript', async (req, res) => {
    try {
        const diffbot_data = await extractDiffbot()

        res.status(200).json(JSON.parse(diffbot_data));

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal Server Error' + error });
    }
});

app.get('/test', async (req, res) => {
    try {
        const topics = [];
        const content = 'This debate is being produced by CNN and it’s coming to you live on CNN, CNN International, CNN.com, CNN Max, and CNN Espanol. This is a pivotal moment between President Joe Biden and former President Donald Trump in their rematch for the nation’s highest office. Each will make his case to the American people with just over four months until Election Day. Good evening. I’m Dana Bash, anchor of CNN’s “Inside Politics” and co-anchor of “State Of The Union.';

        const result = await extractTopics(topics, content);
        const extracted_topics = JSON.parse(result)

        for(const topic of extracted_topics){
            if(topics.includes(topic)){
                
            }
        }
        res.status(200).json(JSON.parse(result));
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal Server Error: \n' + error });
    }
});

async function extractDiffbot() {
    return new Promise((resolve, reject) => {
        console.log('Running Python script for diffbot:');

        const pythonScript = spawn('python3', ['scripts/diffbot_extraction.py']);

        let output = '';
        let errorOutput = '';

        pythonScript.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonScript.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        pythonScript.on('close', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                console.error(`Python script error output: ${errorOutput}`);
                reject(new Error(`Python script failed with code ${code}: ${errorOutput}`));
            }
        });

        pythonScript.on('error', (err) => {
            reject(new Error(`Failed to start subprocess: ${err.message}`));
        });
    });
}

async function extractSentenceData(transcript) {
    return new Promise((resolve, reject) => {
        console.log('Running Python script with transcript in body: ' );

        const pythonScript = spawn('python3', ['scripts/diffbot_extraction.py', transcript]);

        let output = '';
        let errorOutput = '';

        pythonScript.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonScript.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        pythonScript.on('close', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                console.error(`Python script error output: ${errorOutput}`);
                reject(new Error(`Python script failed with code ${code}: ${errorOutput}`));
            }
        });

        pythonScript.on('error', (err) => {
            reject(new Error(`Failed to start subprocess: ${err.message}`));
        });
    });
}

app.post('/texts', async (req, res) => {
    try {
        const weight= await extractWeights(req.body)
        // const clause = await extractClause(req.body)
        const parsedWeight = JSON.parse(weight);
        // const parsedClause = JSON.parse(clause);
        

        res.status(200).json(parsedWeight);

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal Server Error' + error });
    }
});

async function extractWeights(transcript) {
    return new Promise((resolve, reject) => {
        console.log('Running Python script: ' );

        const inputJson = JSON.stringify(transcript);

        const pythonScript = spawn('python', ['scripts/rhetorical.py', inputJson]);

        let output = '';
        let errorOutput = '';

        pythonScript.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonScript.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        pythonScript.on('close', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                console.error(`Python script error output: ${errorOutput}`);
                reject(new Error(`Python script failed with code ${code}: ${errorOutput}`));
            }
        });

        pythonScript.on('error', (err) => {
            reject(new Error(`Failed to start subprocess: ${err.message}`));
        });
    });
}

async function extractClause(transcript) {
    return new Promise((resolve, reject) => {
        console.log('Running Python script: ' );

        const inputJson = JSON.stringify(transcript);

        const pythonScript = spawn('python', ['scripts/clause_data.py', inputJson], {
            encoding: 'utf-8'
        });

        let output = '';
        let errorOutput = '';

        pythonScript.stdout.on('data', (data) => {
            output += data.toString();
        });

        pythonScript.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        pythonScript.on('close', (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                console.error(`Python script error output: ${errorOutput}`);
                reject(new Error(`Python script failed with code ${code}: ${errorOutput}`));
            }
        });

        pythonScript.on('error', (err) => {
            reject(new Error(`Failed to start subprocess: ${err.message}`));
        });
    });
}


// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
