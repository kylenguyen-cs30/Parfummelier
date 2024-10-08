
# frontend/Dockerfile
FROM node:18

WORKDIR /app

COPY package*.json yarn.lock ./

RUN yarn install

COPY . .

EXPOSE 3000

CMD ["yarn", "dev"]

# NOTE: For DEPLOYMENT
#
# frontend/Dockerfile
# FROM node:18
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
# # Build the Next.js app
# RUN yarn build
#
# # Expose the correct port for production
# EXPOSE 3000
#
# # Run the app in production mode
# CMD ["yarn", "start"]
