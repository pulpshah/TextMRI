# How to run the docker

1. Run docker build using this command  
```docker buildx build -t scripts:dev --platform linux/amd64 --target development .```

2. Start the api at port 4001 using this command  
```docker run -p 4001:4001 --name textMRI-API scripts:dev```