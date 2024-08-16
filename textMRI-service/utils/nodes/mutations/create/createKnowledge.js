import { sendMutation } from "../../sendMutation.js";

export async function createKnowledgeNode(type, explanation, text_id) {
    const mutation = `
        mutation {
            createKnowledges(
                input: {
                    type: "${type}"
                    explanation: "${explanation}"
                    textMustHave: { connect: { where: { node: { id: "${text_id}" } } } }
                }
            ) {
                knowledges {
                    type
                    explanation
                }
            }
        }
    `;
    return sendMutation(mutation,{name: `${type} knowledge` ,type: "knowledges"});
}