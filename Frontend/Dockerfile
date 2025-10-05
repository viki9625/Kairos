# Stage 1: Build Stage - Installs dependencies and builds the Next.js app
FROM node:18-alpine AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json to leverage Docker cache
COPY package*.json ./
RUN npm install

# Copy the rest of your app's source code
COPY . .

# Build the Next.js application for production
RUN npm run build

# Stage 2: Production Stage - Creates a small, secure image with only the built app
FROM node:18-alpine

WORKDIR /app

# Copy the built app from the 'builder' stage
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json .
COPY --from=builder /app/next.config.mjs .

# Install only production dependencies
RUN npm install --production

# Expose the port the app runs on
EXPOSE 3000

# The command to start the app
CMD ["npm", "start"]
