
# api-gateway/Dockerfile
FROM kong:latest

COPY kong.yml /app/kong.yml
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/app/kong.yml

CMD ["kong", "docker-start"]
