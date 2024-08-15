import { sendMutation } from "../../../sendMutation.js";

export async function createRhetoricalNode(rhetorical_Weight, document_id) {
    const mutation = `
        mutation {
            createRhetoricalweights(
                input: {
                weight: ${rhetorical_Weight}
                DocumentContains: { connect: { where: { node: { id: "${document_id}" } } } }
                }
            ) {
                rhetoricalweights {
                    rhetorical_weight
                }
            }
        }
    `;
    return sendMutation(mutation, {type: "rhetoricalweights" });
}