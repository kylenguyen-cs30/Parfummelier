
# api-gateway/Dockerfile
FROM kong:latest

# COPY Configuration file into Dockfer
COPY kong.yml /etc/kong/kong.yml

# Turn off Kong Database 
ENV KONG_DATABASE=off

# create Kong Declarative Configuration with Docker
ENV KONG_DECLARATIVE_CONFIG=/etc/kong/kong.yml

CMD ["kong", "docker-start"]
