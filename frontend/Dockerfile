# Use the latest LTS version of Node.js image as base
FROM node:18-slim

# Set working directory
WORKDIR /opt/bibbox_frontend

# Copy the bash script
COPY build.sh ./
COPY health_check.sh ./

# Copy only package.json and package-lock.json first to leverage Docker layer caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --quiet && npm cache clean --force

# Install Angular CLI globally
RUN npm install -g @angular/cli --quiet && ng config -g cli.packageManager yarn


# Make the bash script executable
RUN chmod +x ./build.sh
RUN chmod +x ./health_check.sh

# Set the entrypoint to the bash script
ENTRYPOINT ["./build.sh"]