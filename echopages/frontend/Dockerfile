# Stage 1: Build the React app
FROM node:18 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the React app using a lightweight server
FROM node:18

# Install serve globally
RUN npm install -g serve

# Set the working directory to the build output
WORKDIR /app

# Copy the build output from the previous stage
COPY --from=build /app/build /app

# Expose port 3000 to the outside world
EXPOSE 3000

# Command to run the application
CMD ["serve", "-s", ".", "-l", "3000"]