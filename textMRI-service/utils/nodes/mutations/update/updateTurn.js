import { sendMutation } from "../../sendMutation.js";

export async function updateTopicNode(topic_id, turn_id) {
    const mutation = `
        mutation {
            updateTurns(
                connect: {
                    talkedAboutTopic: {
                        where: {
                            node: {
                                id: "${topic_id}"
                            }
                        }
                    }
                },
                where: { id: "${turn_id}"}
            ) {
                turns {
                    id
                    turn_number
                    content
                }
            }
        }
    `;
    return sendMutation(mutation, { name, type: "turns" }, false);
}
