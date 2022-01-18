### Stage 1: build ###

FROM node:16 AS builder

# Set working directory.
RUN mkdir /app
WORKDIR /app

# Copy app dependencies.
COPY package.json package-lock.json /app/DesafioBRMed-app/

# Install app dependencies.
RUN npm install highcharts-angular --save
RUN npm install highcharts --save
RUN npm install --prefix DesafioBRMed-app

# Copy app files.
COPY . /app

# Default build configuration.
ARG configuration=production

# Build app
RUN npm run build --prefix DesafioBRMed-app -- --output-path=./dist/out --configuration $configuration


### Stage 2: delivery ###

FROM nginx:latest

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy output directory from builder to nginx image.
COPY --from=builder /app/dist/out /usr/share/nginx/html

# Copy nginx configuration file.
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
