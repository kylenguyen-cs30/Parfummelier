# # Use the official Kong Gateway image
# FROM kong:latest
#
# # Copy the Kong configuration files into the container
# COPY kong.yml /kong.yml
# COPY kong.conf /etc/kong/kong.conf
# COPY nginx-kong-template.conf /usr/local/kong/nginx-kong-template.conf
#
# # Set environment variables to run Kong in DB-less mode
# ENV KONG_DATABASE=off
# ENV KONG_DECLARATIVE_CONFIG=/kong.yml
# ENV KONG_NGINX_HTTP_INCLUDE=/usr/local/kong/nginx-kong-template.conf
#
# # Expose the ports for Kong (proxy and admin API)
# EXPOSE 8000 8443
#
# # Start Kong with the custom configuration
# CMD ["kong", "start", "-c", "/etc/kong/kong.conf"]


# Use the official Kong Gateway image
FROM kong:latest

# Copy the Kong configuration files into the container
COPY kong.yml /kong.yml
COPY kong.conf /etc/kong/kong.conf

# Set environment variables to run Kong in DB-less mode
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/kong.yml

# Expose the ports for Kong (proxy and admin API)
EXPOSE 8000 8443

# Start Kong with the custom configuration
CMD ["kong", "start", "-c", "/etc/kong/kong.conf"]

