# # frontend/Dockerfile
#
# FROM node:lts
#
# # Install Yarn globally (ensure it is available)
# # RUN npm install -g yarn
#
# WORKDIR /app
#
# # Copy package files
# COPY package*.json yarn.lock ./
#
# # Install dependencies
# RUN yarn install
#
# # Copy the entire project
# COPY . .
#
# # Build the Next.js app (if in production mode)
# # ARG NODE_ENV=development
# # RUN if [ "$NODE_ENV" = "production" ]; then yarn build; fi
#
# # Expose the correct port
# EXPOSE 3000
#
# # CMD to run the app in the correct mode
# CMD ["yarn", "dev"] # For development
#
# # Uncomment for production
# # CMD ["yarn", "start"] # For production

# frontend/Dockerfile

FROM node:lts

WORKDIR /app

# Copy package files
COPY package*.json yarn.lock ./

# Install dependencies
RUN yarn install

# Copy the entire project
COPY . .

# Expose the correct port
EXPOSE 3000

# CMD to run the app in the correct mode
CMD ["sh", "-c", "yarn dev"] # For development mode

# Uncomment for production
# CMD ["sh", "-c", "yarn start"] # For production mode

