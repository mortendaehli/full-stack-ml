# syntax=docker/dockerfile:1
FROM node:16-alpine as dev

ARG USER_ID=1000
ARG USER_GROUP=1000
ARG NODE_ENV=prod

ENV CI=true

RUN npm install -g npm@7

RUN deluser --remove-home node \
 && addgroup -S notroot -g $USER_GROUP \
 && adduser -u $USER_ID -G notroot -S notroot \
 && mkdir /code \
 && chown notroot:notroot /code

USER notroot
WORKDIR /projects/frontend/

COPY --chown=notroot:notroot projects/frontend/package.json projects/frontend/package-lock.json ./

COPY --chown=notroot:notroot projects/frontend/ ./


FROM dev as build

RUN npm ci

RUN npm run build

FROM bitnami/nginx:1.21 as deploy

COPY --from=build /projects/frontend/build /var/www/data
COPY --from=build /projects/frontend/nginx.conf /opt/bitnami/nginx/conf/server_blocks/nginx-deploy.conf
