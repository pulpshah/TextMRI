import { sendMutation } from "../../sendMutation.js";

export async function createDocumentNode(turn_number, content, speaker, role, text_id) {
    const mutation = `
        mutation {
            createDocuments(
                input: {
                turn_number: ${turn_number}
                content: "${content}"
                speaker: "${speaker}"
                role: "${role}"
                textHas: { connect: { where: { node: { id: "${text_id}" } } } }
                }
            ) {
                documents {
                    id
                    turn_number
                    content
                }
            }
        }
    `;
    return sendMutation(mutation, { name: `Document #${turn_number}`, type: "documents" });
}
