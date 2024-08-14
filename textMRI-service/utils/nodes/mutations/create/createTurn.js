import { sendMutation } from "../../sendMutation.js";

export async function createTurnNode(turn_number, content, transcript_id, actor_id) {
    const mutation = `
        mutation {
            createTurns(
                input: {
                    turn_number: ${turn_number},
                    content: "${content}",
                    texttranscriptMustContain: {
                        connect: {
                            where: {
                                node: {
                                    id: "${transcript_id}"
                                }
                            }
                        }
                    }
                    actorSpokeIn: {
                        connect: {
                            where: {
                                node: {
                                    id: "${actor_id}"
                                }
                            }
                        }
                    }
                }
            ){
            turns {
                id,
                turn_number,
                content
            }
        }
    }
  
  `;
    return sendMutation(mutation, { name: `Turn #${turn_number}`, type: "turns" });
}
