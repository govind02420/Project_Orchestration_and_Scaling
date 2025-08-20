# syntax=docker/dockerfile:1.6
FROM node:18-alpine

ENV NODE_ENV=production
WORKDIR /usr/src/app

# Install dependencies (use npm ci, cache npm)
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production --no-audit --fund=false

# Copy the app (exclude .env via .dockerignore)
COPY . .

# Expose profile-service port
EXPOSE 3002

# Do NOT bake env secrets into the image
# Inject PORT and MONGO_URL at runtime via env or compose/k8s
CMD ["node", "index.js"]
