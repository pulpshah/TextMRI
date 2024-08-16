import axios from "axios";
import { API_URL } from "../neo4j_API_URL.js";
import dotenv from "dotenv";
dotenv.config();

// Sends a mutation to the Neo4j database
export async function sendMutation(mutation, { name, type }, create = true) {
    // console.log(mutation)
    try {
        const response = await axios.post(API_URL, {
            query: mutation,
        });

        const mutationName = `${create ? "create" : "update"}${capitalizeString(type)}`
        if(response.data.errors) throw new Error(`Error sending ${name} mutation: \n`, response.data.errors[0].message);
        
        if(process.env.LOG == "EXPAND") console.LOG(`Successfully ${create ? "created" : "updated"} ${name} for ${type} mutation: \n`, response.data.data[mutationName][type]) 
        else if(process.env.LOG == "REDUCED") console.log(`Successfully ${create ? "created" : "updated"} ${name} for ${type} mutation`);

        if(create) return response.data.data[mutationName][type];
    } catch (error) {
        console.error(`Error sending ${name} mutation: \n`, error.message);
        throw new Error(`Error sending ${name} mutation: \n`, error.message)
    }
}

function capitalizeString(str){
    return str.charAt(0).toUpperCase() + str.slice(1);
}
 