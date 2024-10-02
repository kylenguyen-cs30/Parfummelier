
# api-gateway/Dockerfile
FROM kong:latest

# COPY Configuration file into Dockfer
COPY kong.yml /app/kong.yml

# Turn off Kong Database 
ENV KONG_DATABASE=off

# create Kong Declarative Configuration with Docker
ENV KONG_DECLARATIVE_CONFIG=/app/kong.yml

CMD ["kong", "docker-start"]
