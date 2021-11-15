# syntax=docker/dockerfile:1
FROM node:16-alpine as dev

RUN npm install -g npm@7

WORKDIR /code

COPY projects/frontend/package.json projects/frontend/package-lock.json ./

RUN npm ci

COPY projects/frontend/ ./

FROM dev as build

RUN npm run build

FROM bitnami/nginx:1.21 as deploy
COPY --from=build /code/build /app
COPY --from=build /code/nginx_server_block.conf /opt/bitnami/nginx/conf/server_blocks/my_server_block.conf
