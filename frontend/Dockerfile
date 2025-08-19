# Use Apache httpd as the web server
FROM httpd:2.4-alpine
# Copy static site into Apache's document root
COPY index.html /usr/local/apache2/htdocs/index.html
# Exposes port 80 by default in the base image