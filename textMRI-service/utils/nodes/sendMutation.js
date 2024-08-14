import axios from "axios";
import { API_URL } from "../neo4j_API_URL.js";

export async function sendMutation(mutation, { name, type }, returnData = true) {
    // console.log(mutation)
    try {
        const response = await axios.post(API_URL, {
            query: mutation,
        });

        const mutationName = `create${capitalizeString(type)}`
        console.log(`Successfully ${returnData ? "created" : "updated"} ${name} for ${type} mutation: \n`, response.data.data[mutationName][type]);
        if(returnData) return response.data.data[mutationName][type];
    } catch (error) {
        console.error(`Error sending ${name} mutation: \n`, error.message);
        return `Error sending ${name} mutation: \n`, error.message
    }
}

function capitalizeString(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}