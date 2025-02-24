# quantee_recruitment_task

## Prepare the environment

Clone repository and move to it
```shell
git clone https://github.com/ArtemKart/quantee_recruitment_task.git
cd quantee_recruitment_task
```

Check if make is already installed 

```shell
make --version
```

If not but I want to, install:
```shell
sudo apt install make
```
### Make stages

Install virtual environment and all dependencies
```shell
make install
```

Run linters check (black, pylama)
```shell
make lint
```

If you're not a Make Person, you can install dependencies directly:
```shell
python -m venv .venv
source .venv/bin/activate 
# use `.venv\Scripts\activate` if you're Windows user
python -m pip install --upgrade pip && pip install .
```

If you're going to develop the application, run:
```shell
python -m pip install --upgrade pip && pip install .[dev]
```

## Create .env file

You can create `.env` file by copying from `.env-template`:
```shell
cp .env-template .env
```

That's how `.env` file looks like:
```text
POSTGRES_USER=postgres user
POSTGRES_PASSWORD=postgres password
POSTGRES_DB=postgres database name
POSTGRES_HOST=postgres host address
POSTGRES_PORT=postgres port

USE_PROXY=use proxy
STORAGE_ROOT_DIR=path to set as storage dir as volume
```
Provide your own values following the description

## Start application in Docker

Make sure your Docker is already installed. If not, install it downloading Docker.exe
file from https://www.docker.com/ or any another way

Check if docker installed:
```shell
docker --version
# Docker version 27.5.1, build 9f9e405
docker compose version
# Docker Compose version v2.32.4-desktop.1
```

To up the docker containers, configured in `docker-compose.yml` file, run:
```shell
docker compose up
```

Afterward, you can achieve the backend side of application using Swagger Documentation: http://localhost/api/v1/docs

## Hints & Tips:

1. With base `docker-compose.yml` config, you won't be able to connect to database in docker container locally. 
To achieve that, set ports to `database` service in `docker-compose.yml`:
```yaml
ports:
  -  "5432:5432" # set your ports here
```
2. Inside a docker network, you can achieve a connection to database using database service name 
in `docker-compose.yml` as environmental variable `POSTGRES_HOST`
3. To test the system's scalability, you can run `docker compose up` using `--scale client=X` argument 
to create X containers. Test files have already prepared in `tests/load` folder:
```shell
cd tests/load
docker compose up --scale client=6
```
