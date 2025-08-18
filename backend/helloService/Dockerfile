FROM node:18-alpine

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install --production

COPY . .

# Load environment from .env
ENV PORT=3001

EXPOSE 3001

CMD ["node", "index.js"]
