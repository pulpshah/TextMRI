import { sendMutation } from "../../../sendMutation.js";

export async function createClarityNode({score, readability_score, readability_explanation, grammar_score, grammar_explanation}, document_id ){
    const mutation = `
    mutation {
      createClarities(input: {
        score: ${score}
        readabilityContributesTo: {
          create: {
            node: {
              readability_score: ${readability_score}
              explanation: "${readability_explanation}"
            }
          }
        }
        grammarContributesTo: {
          create: {
            node: {
              grammar_score: ${grammar_score}
              explanation: "${grammar_explanation}"
            }
          }
        }
        documentMustContain: {
          connect: { where: { node: { id: "${document_id}" } } }
        }
      }) {
        clarities {
          score
        }
      }
    }
    `;
    return sendMutation(mutation, { name: `Clarity ${score}`, type: "clarities" });
}
