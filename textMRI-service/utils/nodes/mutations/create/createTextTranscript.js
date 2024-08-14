import { sendMutation } from "../../sendMutation.js";

export async function createTextTranscriptNode(name) {
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
    return sendMutation(mutation, { name, type: "textTranscripts" });
}
