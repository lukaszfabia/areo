#!/bin/bash

if [[ -z $1 ]]
then 
    echo "usage: migrate <migration name>"
    exit 1 
fi


source ../.env 

echo "Loaded from .env:"
echo -e "\t$POSTGRES_USER\n\t$POSTGRES_PASSWORD\n\t$POSTGRES_DB\n\t$POSTGRES_PORT\n\t$POSTGRES_HOST"

alembic revision --autogenerate -m "$1"
alembic upgrade head
