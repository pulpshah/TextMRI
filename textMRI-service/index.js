import express from 'express';
import { request, gql } from 'graphql-request';
import bodyParser from 'body-parser';
import { spawn } from 'child_process';

const app = express();
app.use(bodyParser.json());

app.post('/transcript', async (req, res) => {
    const { transcript } = req.body;

    if (!transcript) {
        return res.status(400).json({ error: 'Transcript is required' });
    }
    // console.log('Transcript:', transcript);
    try {
        const result = await runMLScript(JSON.stringify(transcript));

        // 2. Prepare GraphQL mutation with ML results
        // const mutation = gql`
        //     mutation($input: [TextTranscriptCreateInput!]!) {
        //         createTextTranscripts(input: $input) {
        //             textTranscripts {
        //                 name
        //             }
        //         }
        //     }
        // `;

        // const variables = {
        //     input: [
        //         {
        //             name: result.name
        //         }
        //     ]
        // };

        // const endpoint = 'http://localhost:4000/';
        // const response = await request(endpoint, mutation, variables);

        res.status(200).json(JSON.parse(result));
    } catch (error) {
        console.error('Error processing transcript:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

async function runMLScript(transcript) {
    return new Promise((resolve, reject) => {
        console.log('Running Python script with transcript:');

        const pythonScript = spawn('python3', ['scripts/sentence_data.py', transcript]);

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
