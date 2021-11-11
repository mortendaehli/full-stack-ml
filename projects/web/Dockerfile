FROM node:16-alpine as dev

ARG USER_ID=502
ARG USER_GROUP=1000

RUN npm install -g npm@7

RUN deluser --remove-home node \
 && addgroup -S notroot -g USER_GROUP \
 && adduser -u USER_ID -G notroot -S notroot \
 && mkdir /code \
 && chown notroot:notroot /code

USER notroot
WORKDIR /code

COPY --chown=notroot:notroot projects/web/package.json projects/web/package-lock.json ./

RUN npm ci --ignore-scripts

ENV CI=true

COPY --chown=notroot:notroot projects/web/ ./

EXPOSE 3000

CMD ["npm", "start"]

FROM dev as build

RUN npm run build

FROM bitnami/nginx:1.21 as deploy
COPY --from=build   /code/build                 /var/www/data
COPY projects/web/nginx-deploy.conf             /opt/bitnami/nginx/conf/server_blocks/nginx-deploy.conf
