# Use Node.js base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the code
COPY . .

# Build production files
RUN npm run build

# Serve using a lightweight server
RUN npm install -g serve
CMD ["serve", "-s", "dist"]

EXPOSE 5173
