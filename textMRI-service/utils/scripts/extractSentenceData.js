import { spawn } from 'child_process';

export async function extractSentenceData(transcript) {
    return new Promise((resolve, reject) => {
        console.log("Running Python script with transcript in body: ");

        const pythonScript = spawn("python3", [
            "scripts/diffbot_extraction.py",
            transcript,
        ]);

        let output = "";
        let errorOutput = "";

        pythonScript.stdout.on("data", (data) => {
            output += data.toString();
        });

        pythonScript.stderr.on("data", (data) => {
            errorOutput += data.toString();
        });

        pythonScript.on("close", (code) => {
            if (code === 0) {
                resolve(output);
            } else {
                console.error(`Python script error output: ${errorOutput}`);
                reject(
                    new Error(
                        `Python script failed with code ${code}: ${errorOutput}`
                    )
                );
            }
        });

        pythonScript.on("error", (err) => {
            reject(new Error(`Failed to start subprocess: ${err.message}`));
        });
    });
}