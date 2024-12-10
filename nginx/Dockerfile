# Dockerfile

FROM nginx:1.27.3
# Delete the default configuartion file that comes with the offical image
RUN rm /etc/nginx/conf.d/default.conf
# Copy the configuartion file into the container
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir -p /etc/nginx/ssl
# Erstelle das Verzeichnis für die Zertifikate
RUN mkdir -p /etc/nginx/ssl

# generate self signed certificates with openssl
RUN openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/privkey.pem \
    -out /etc/nginx/ssl/fullchain.pem \
    -subj "/CN=localhost"

# set the correct rights for the certificates
RUN chmod 600 /etc/nginx/ssl/privkey.pem /etc/nginx/ssl/fullchain.pem