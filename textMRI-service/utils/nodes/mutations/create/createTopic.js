import { sendMutation } from "../../sendMutation.js";

export async function createTopicNode(name, transcript_id) {
    const mutation = `
        mutation {
        createTopics(
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
            topics {
                id,
                name
            }
        }
    }

`;
    return sendMutation(mutation, { name, type: "topics" });
}