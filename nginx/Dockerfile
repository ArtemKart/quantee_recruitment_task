FROM alpine:latest AS base

WORKDIR /workspace
COPY . .
RUN apk --no-cache add gettext
COPY nginx.conf-template /etc/nginx.conf
RUN dos2unix /etc/nginx.conf

FROM nginx:stable

RUN rm /etc/nginx/nginx.conf
COPY --from=base /etc/nginx.conf /etc/nginx/nginx.conf
