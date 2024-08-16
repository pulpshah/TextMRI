import { sendMutation } from "../../sendMutation.js";

export async function updateTurnNodeWithTopics(topic_id, turn_id) {
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
    return sendMutation(mutation, { name: `topic id: ${turn_id} relationship for turn node`, type: "turns" }, false);
}
