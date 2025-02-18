# Use official Node.js image as base
FROM node:16

# Set the working directory inside the container
WORKDIR /user_service

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Install Prisma
RUN npx prisma generate

# Expose the port your app will run on
EXPOSE 3000

# Start the application
CMD ["npm", "run", "dev"]
