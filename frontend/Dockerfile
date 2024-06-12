# Use a lightweight web server image
FROM nginx:alpine

# Remove the default Nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy the frontend files to the Nginx directory
COPY . /usr/share/nginx/html

# Expose the port that Nginx will run on
EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
