FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Ensure environment file is copied
COPY .env.local ./

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
