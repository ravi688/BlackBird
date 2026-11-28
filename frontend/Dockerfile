# Build React frontend
FROM node:24-alpine AS frontend-build

WORKDIR /blackbird

COPY blackbird/package*.json ./
RUN npm ci

COPY blackbird/ ./

RUN npm run build


# Nginx reverse proxy + static frontend
FROM nginx:alpine

COPY ngnix.conf /etc/nginx/conf.d/default.conf

COPY --from=frontend-build /blackbird/dist /usr/share/nginx/html

EXPOSE 80
