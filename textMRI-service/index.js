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

    try {
        const result = await extractSentenceData(JSON.stringify(transcript));

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

app.get('/texts', async (req, res) => {
    try {
        // Define the GraphQL query to get all text nodes
        const query = gql`
            {
                texts {
                    name
                    
                }
            }
        `;

        // Replace with your GraphQL endpoint
        const endpoint = 'http://localhost:4000';

        // Execute the query
        const data = await request(endpoint, query);

        // Send the data back as the response
        res.status(200).json(data);
    } catch (error) {
        console.error('Error fetching text nodes:', error);
        res.status(500).json({ error: 'Failed to fetch text nodes' });
    }
});

app.get('/text', async (req, res) => {
    try {
        const { name } = req.query; // Get the 'name' parameter from the query string

        if (!name) {
            return res.status(400).json({ error: 'Name query parameter is required' });
        }

        // Define the GraphQL query to get text nodes by name
        const query = gql`
            query GetTextsByName($name: String!) {
                texts(where: { name: $name }) {
                    name
                   
                }
            }
        `;

        // Replace with your GraphQL endpoint
        const endpoint = 'http://localhost:4000';

        // Execute the query with the name as a variable
        const data = await request(endpoint, query, { name });

        // Send the data back as the response
        res.status(200).json(data);
    } catch (error) {
        console.error('Error fetching text nodes:', error);
        res.status(500).json({ error: 'Failed to fetch text nodes' });
    }
});

// app.get('/textid', async (req, res) => {
//     try {
//         const { id } = req.query; // Get the 'id' parameter from the query string

//         if (!id) {
//             return res.status(400).json({ error: 'ID query parameter is required' });
//         }

//         // Define the GraphQL query to get a text node by id
//         const query = gql`
//             query GetTextById($id: ID!) {
//                 text(where: { id: $id }) {
//                     id
//                     name

//                 }
//             }
//         `;

//         // Replace with your GraphQL endpoint
//         const endpoint = 'http://localhost:4000';

//         // Execute the query with the id as a variable
//         const data = await request(endpoint, query, { id });

//         // Send the data back as the response
//         res.status(200).json(data);
//     } catch (error) {
//         console.error('Error fetching text node:', error);
//         res.status(500).json({ error: 'Failed to fetch text node' });
//     }
// });

app.get('/text-documents', async (req, res) => {
    try {
        const { name } = req.query; // Get the 'name' parameter from the query string

        if (!name) {
            return res.status(400).json({ error: 'Name query parameter is required' });
        }

        // Define the GraphQL query to get documents by text name
        const query = gql`
            query GetDocumentsByTextName($name: String!) {
                texts(where: { name: $name }) {
                    name
                    documents {
                        role
                        content
                        speaker
                        rhteroical_weight
                    }
                }
            }
        `;

        // Replace with your GraphQL endpoint
        const endpoint = 'http://localhost:4000';

        // Execute the query with the name as a variable
        const data = await request(endpoint, query, { name });

        // Send the data back as the response
        res.status(200).json(data);
    } catch (error) {
        console.error('Error fetching documents for text node:', error);
        res.status(500).json({ error: 'Failed to fetch documents for text node' });
    }
});


// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
