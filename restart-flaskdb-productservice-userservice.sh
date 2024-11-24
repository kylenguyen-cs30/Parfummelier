#!/bin/bash

# Remove existing migrations and initialize the database for product-service
docker-compose exec product-service bash -c "
    rm -rf migrations/ &&
    flask db init &&
    flask db migrate -m 'Initial Migration' &&
    flask db upgrade
"

# Remove existing migrations and initialize the database for user-service
docker-compose exec user-service bash -c "
    rm -rf migrations/ &&
    flask db init &&
    flask db migrate -m 'Initial Migration' &&
    flask db upgrade
"
