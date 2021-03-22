FROM node:lts-alpine as build-stage
WORKDIR /smait
COPY package*.json ./

RUN npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine as production-stage
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

COPY --from=build-stage ./smait/dist /usr/share/nginx/html/smait
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]