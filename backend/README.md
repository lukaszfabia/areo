# How to run me

Install docker, docker-compose, then run docker-compose.yml with env vars.

run migration.sh

to go into db 

docker exec -it <container> psql -U <user> -d <db>

run server with unicorn!

uvicorn app:main.py 



