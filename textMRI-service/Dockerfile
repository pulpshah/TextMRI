FROM nikolaik/python-nodejs:latest AS development
WORKDIR /usr/src/app
RUN pip install pandas 
COPY ./package.json ./
RUN npm install
COPY ./ ./
# RUN npm run build
ENV PORT=4001
EXPOSE $PORT
CMD ["npm", "run", "dev"]


#Production mode
FROM nikolaik/python-nodejs:latest AS production
RUN pip install pandas
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}
WORKDIR /usr/src/app
COPY --from=development /usr/src/app ./
ENV PORT 4000
EXPOSE $PORT
CMD ["node", "dist/main"]