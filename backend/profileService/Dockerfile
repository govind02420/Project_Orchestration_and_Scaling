FROM node:18-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --production

COPY . .

# Load environment from .env
ENV PORT=3002
# NOTE: Update this with actual Mongo URL during deployment
ENV MONGO_URL="specifyYourMongoURLHereWithDatabaseNameInTheEnd"

EXPOSE 3002

CMD ["node", "index.js"]
