FROM node:18.16.1 as DIST

ARG MYENV
WORKDIR /design
COPY design .
RUN npm install --no-progress --registry=http://192.168.0.79:4873/ \
    && npm run v-build

FROM nginx:1.19.3-alpine
COPY ./docker/web/nginx.conf /etc/nginx/conf.d/design.conf
COPY --from=DIST /design/dist /usr/share/nginx/html
