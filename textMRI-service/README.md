# How to run the docker(Depreciated)

Look at the main README.md file to create a docker container and image
1. Run docker build using this command    
~~```docker buildx build -t scripts:dev --platform linux/amd64 --target development .```~~

2. Start the api at port 4001 using this command  
~~```docker run -p 4001:4001 --name textMRI-API scripts:dev```~~

# Next Steps

1. **Add typescript support**  
Refactor the code for typescript. As this API as been expanding, the code becomes more complex and easier to misinterpret. By adding typescript, a lot of these problems can me mitigated.

2. **Optimizing Node Creation**  
Right now, we are creating nodes dynamically where each node is created one at a time.
One way to optimize this is to refactor the code so that it can create all the prerequisite(independent) nodes at the same time by passing an array through the mutation 

**Note:** The graphql schema is based off the pulp information object on arrows.app, however the schema has been modified. The automatic schema generation on arrows.app cannot support more complex relationships like one to many(it supports many to one though). As a result, changes should be made to both the schema and arrows.app if possible to keep both similar.

3. **Authentication and Authorization**  
Add Authentication so that only users that are logged in can perform queries/mutations
Add Role Based Access Control so that only users with specific roles can perform specific queries and mutations(Authorization)

4. **Integrate additional scripts**  
Once the other scripts are finished, integrate it with our API so that the nodes tied with those scripts can be generated

5. **Decoupling**   
Seperate the upload of the transcript from the processing of the transcript. I have attached a link to a figma that could be used as the architecture of the TextMRI api.  
[Architecture Design](https://www.figma.com/design/46QoQnWCgsIE8SbwWHJPSn/TextMRI-API-Design?node-id=2202-191&t=ZQemVyjJbOP5NTss-1)  
The goal is to allow the user to upload the transcript and leave the page. The API will split the transcript up and process it asynchronously and/or concurrently.  
After the entire script is finished processing, send a notification to the user through a webhook