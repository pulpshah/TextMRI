import { sendMutation } from "../../sendMutation.js";

export async function createHumorNode(score, explanation, document_id ){
    const mutation = `
    mutation {
      createHumors(
        input: {
          score: "${score}"
          explanation: "${explanation}"
          documentMustContain: { connect: { where: { node: { id: "${document_id}" } } } }
        }
      ) {
        Humors {
          score,
          explanation
      }
    }

  `;
    return sendMutation(mutation, { name: `Humor ${score}`, type: "Humors" });
}
