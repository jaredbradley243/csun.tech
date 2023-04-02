FROM node:19-bullseye-slim

WORKDIR /csuntech

COPY package.json .

COPY package-lock.json .

RUN npm install
RUN apt-get update && apt-get install -y git

COPY . .

EXPOSE 3000

CMD [ "npm", "start" ]
