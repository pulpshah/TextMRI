## Overview
The TextMRI API provides tools to analyze debates using technology that will eventually be packaged into the Pulp SDK. 

This API can be used to retrieve statistics, information about speeches, persuasive resonance, and more. Users can select a debate and access detailed information about it, including the host, location, date, time, speakers, and their talk times. Additionally, the API provides a transcript of the debate with detailed metadata and a reference bank for relevant articles, PDFs, videos, or images.

### How to run using Docker 
**NOTE:** Please have Docker Desktop and Docker Compose installed

1. run ```docker compose build```
2. run ```docker compose up```
3. now the neo4j-service is up and running at port 4000 and the textMRI-service is up and running at port 4001.  
If you are trying to get queries/perform mutations you can send the request directly to the neo4j service. If you are trying to update a transcript to be generated, send it to port 4001 /transcript e.g. http://localhost:4001/transcript.  
In the body there should be JSON sent through in the following format. 
```json
{
    "transcript": {
        "name": "your_transcript_name",
        "debate": [
            {
                "speaker": "speaker_name",
                "role": "role",
                "content": "content",
                "turn_number": Integer
            }
        ]
    }
}
```
**Note:** This might change depending on how the data is being scrapped/gathered

### Product Requirements
1. Conversation Ingestion/processing
2. Interactive Conversation Text/Transcripts
3. Automated Exploratory Data Analyses
4. Export Functionality
5. Persuasive Resonance Visualizer
6. LLM Chatbot Integration

### Database

#### ACID
Atomicity, Consistency, Isolation, Durability 

1. Atomicity - “All or nothing” if a transaction fails half way, rollback the transaction to prevent data corruption 
2. Consistency - preserving database invariants( reject requests that don’t conform to our database rules e.g. liking a comment twice should not happen)
3. Isolation - Concurrent transactions are hidden from each other. I.e. if one user is trying to like a comment and another user is trying to get a list of all the likes in that comment at the same time. The second user should not be able to see the first users like, in case the first users transaction fails
4. Durability - Data persists after a transaction is committed, even after failure. In cloud storing, have multiple copies of the database so incase the db goes down, it doesn’t affect the website 

#### Database Provider

**Neo4j AuraDB**  
Cloud service provider for neo4j
https://console.neo4j.io/

Installation
https://neo4j.com/docs/operations-manual/current/installation/

Neo4j desktop for developing
https://neo4j.com/download/

#### E-R diagram

### Authentication/Authorization

NextAuth

#### Roles/Scopes

#### Example Setup
Front end can use as reference to send JWT tokens to server(An outdated version of Next.Js, uses Page router instead of App router)  
https://arunoda.me/blog/add-auth-support-to-a-next-js-app-with-a-custom-backend


### Hosting


## API Documentation

### API Architecture

**GraphQL**

Pros
1. Prevents overfetching/underfetching(Effecient Queries)
2. Seamless Integration
3. Efficiency in Data Retrieval 

Cons  
1. N+1 Query Problem
2. Query Optimization
3. Error handling


**Webhooks**

### AI Chatbot

### API V0

#### What will our API provide?
1. TextMRI -> Main Aspects
Conversation ingestion - Intakes URLs, JSON objects, PDFs, Images, and eventually videos and outputs the Pulp Conversation Object
What will the Pulp Conversation Object look like?

2. (Main tab in the webapp) Interactive conversation text/transcripts

3. (2nd tab in the webapp) Automated Exploratory Data Analyses - references an ingested conversation and lets user choose to either conversationally ask or technically configure one or more hypothesis statements and returns a fully annotated and interactive EDA with written, statistical, visual, and predictive aspects formatted and displayed for heavy user engagement

4. Export - Lets the user export the results of an EDA via PDF or HTML file

5. (3rd tab in the webapp) Persuasive Resonance Visualizer - lets user configure and contextualize speaker/audiences with various customizable/randomizable input fields for various psychographic, demographic, and mind-state related data; once configured, the user can predict and visualize ICP sentiment in specific scenarios

6. Chatbot name TBD - LLM linked to a vector db to continue further conversational exploration
