import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { Neo4jGraphQL } from "@neo4j/graphql";
import neo4j from "neo4j-driver";
import dotenv from "dotenv";
dotenv.config();

const typeDefs = `#graphql
    # type Movie {
    #     title: String
    #     actors: [Actor!]! @relationship(type: "ACTED_IN", direction: IN)
    # }

    # type Actor {
    #     name: String
    #     movies: [Movie!]! @relationship(type: "ACTED_IN", direction: OUT)
    # }
`;

const driver = neo4j.driver(
    process.env.NEO4J_URI,
    neo4j.auth.basic(process.env.NEO4J_USERNAME, process.env.NEO4J_PASSWORD)
);

const neoSchema = new Neo4jGraphQL({ typeDefs, driver });

const server = new ApolloServer({
    schema: await neoSchema.getSchema(),
});

const { url } = await startStandaloneServer(server, {
    listen: { port: 4000 },
});

console.log(`🚀 Server ready at ${url}`);