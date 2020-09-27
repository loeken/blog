FROM nginx:alpine
COPY public/ /usr/share/nginx/html/
COPY nginx_conf.d/ /etc/nginx/conf.d/
