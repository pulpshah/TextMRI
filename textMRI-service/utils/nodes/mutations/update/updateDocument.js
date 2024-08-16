import { sendMutation } from "../../sendMutation.js";

export async function updateDocumentNodeWithTopics(topic_id, document_id) {
    const mutation = `
        mutation {
            updateDocuments(
                connect: { mustContainTopic: { where: { node: { id: "${topic_id}" } } } }
                where: { id: "${document_id}" }
            ) {
                documents {
                    id
                    turn_number
                    content
                    speaker
                    role
                }
            }
        }
    `;
    return sendMutation(mutation, { name: `topic id: ${document_id} relationship for document node`, type: "documents" }, false);
}
