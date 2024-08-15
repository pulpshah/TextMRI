import { spawn } from 'child_process';
import dotenv from "dotenv";
dotenv.config();

export async function extractClause(transcript) {
    return new Promise((resolve, reject) => {
        console.log('Running Python script: ' );

        const inputJson = JSON.stringify(transcript);
        const pythonScript = spawn('python3', ['scripts/clause_data.py', inputJson], {
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