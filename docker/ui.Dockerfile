# build stage
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY src/ui/Useless_Machine ./
RUN npm install
RUN npm run build


# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY src/ui/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
