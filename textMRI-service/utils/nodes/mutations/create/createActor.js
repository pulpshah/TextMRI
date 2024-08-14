import { sendMutation } from "../../sendMutation.js";

export async function createActorNode( name, role, transcript_id) {
    const mutation = `
        mutation {
            createActors(
                input: {
                    name: "${name}",
                    role: "${role}",
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
                actors {
                    id,
                    name,
                    role
                }
            }
        }

    `;
    return sendMutation(mutation, { name, type: "actors" });
}