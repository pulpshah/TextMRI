import { sendMutation } from "../../sendMutation.js";

export async function createClarityNode(score, readability_score, readability_expl, grammar_score, grammar_expl, document_id ){
    const mutation = `
    mutation {
      createClarities(
        input: {
          score: "${score}"
          readability_score: "${readability_score}"
          readability_expl: "${readability_expl}"
          grammar_score: "${grammar_score}"
          grammar_expl: "${grammar_expl}"
          documentMustContain: { connect: { where: { node: { id: "${document_id}" } } } }
        }
      ) {
        clarities {
          score,
          readability_score
          readability_expl
          grammar_score
          grammar_expl
        }
      }
    }

  `;
    return sendMutation(mutation, { name: `Clarity ${score}`, type: "clarities" });
}
