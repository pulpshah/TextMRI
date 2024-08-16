// Return an array of unique speakers from a debate

export function extractUniqueSpeakers(debate) {
    const speakers = {};

    debate.forEach(entry => {
        const { speaker, role } = entry;
        if (!speakers[speaker]) {
            speakers[speaker] = role;
        }
    });

    return Object.entries(speakers).map(([speaker, role]) => ({ name: speaker, role }));
}