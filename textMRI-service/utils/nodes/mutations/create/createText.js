import { sendMutation } from "../../sendMutation.js";

export async function createTextNode(name, transcript_id) {
    const mutation = `
        mutation {
            createTexts(
                input: {
                name: "${name}",
                texttranscriptMustContain: {
                    connect: {
                        where: {
                            node: {
                                id: "${transcript_id}"
                            }
                        }
                    }
                }
            }
            
        ) {
            texts {
            id,
            name
            }
        }
        }
    `;
    return sendMutation(mutation, { name, type: "texts" });
}
