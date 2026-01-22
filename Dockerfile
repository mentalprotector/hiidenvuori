FROM nginx:alpine

# Copy static assets
COPY . /usr/share/nginx/html

# Custom Nginx config to handle clean URLs (optional but good for /contacts instead of /contacts.html)
# For now, default is fine since we have .html in links, 
# but let's make sure it serves index.html for root.
