### Development Guidelines for Odoo Inside Docker

#### 0. Begin

```sh
mkdir proj-dir
cd proj-dir
```

#### 1. Write the `docker-compose.yaml` file

Create a [docker-compose.yaml](docker-compose.yaml) with the following content:

```yaml
version: '3.1'

services:
  db:
    image: postgres:latest
    container_name: postgres_db
    restart: always
    ports:
      - "5444:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres_pwd
      - POSTGRES_DB=postgres
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./init-db.sh:/docker-entrypoint-initdb.d/init-db.sh
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -h localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  odoo:
    image: odoo:17.0
    container_name: odoo_app
    restart: always
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - PORT=5432
      - USER=test_usr
      - PASSWORD=test_pwd
    volumes:
      - web-data:/var/lib/odoo
      - ./extra-addons:/mnt/extra-addons
    depends_on:
      - db
    command: ["-i", "base", "-d", "project_db"]

volumes:
  db-data:
  web-data:
```

#### 2. Run Docker Compose

Build and start the containers with the following command:

```sh
docker-compose up --build --remove-orphans
# Because of the mount inside the docker-compose file, this command will create `extra-addons` dir inside `proj-dir`
```

#### 3. Adjust the Ownership of `extra-addons` Directory

Create a [Makefile](Makefile) with the following content:

```makefile
LOCAL_USER := $(shell id -u):$(shell id -g)
DOCKER_EXEC := docker exec -it -u root odoo_app

local-chown:
	sudo chown -R $(LOCAL_USER) extra-addons

docker-chown:
	$(DOCKER_EXEC) chown -R odoo:odoo /mnt/extra-addons

.DEFAULT_GOAL := help

help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  local-chown    : Change ownership of 'extra-addons' locally"
	@echo "  docker-chown   : Change ownership of '/mnt/extra-addons' inside Docker container"
	@echo "  help           : Show this help message"
```

To work locally, run:

```sh
make local-chown # sudo chown -R 1000:1000 extra-addons
```

To work inside the container, run:

```sh
make docker-chown # docker exec -it -u root odoo_app chown -R odoo:odoo /mnt/extra-addons
```

In case you face an error not having the `odoo` group, run:

```sh
sudo groupadd odoo
sudo usermod -aG odoo $USER
```

#### 4. Confirm Permissions

Check the permissions of the `extra-addons` directory locally and inside the Docker container:

**Local Directory**

```sh
make local-chown

mkdir extra-addons/app1 # Now should work from local too without permission error
# Sample output
❯ ls -l extra-addons
total 4
drwxrwxr-x 2 abdi abdi 4096 Jul  2 17:06 app1
```

**Docker Container Directory**

```sh
make docker-chown
```

Then, access the container:

```sh
docker exec -it odoo_app bash
```

Inside the container:

```sh
odoo@container:/$ odoo scaffold app2 /mnt/extra-addons
odoo@container:/$ ls -l /mnt/extra-addons
# Sample output
total 8
drwxrwxr-x 2 odoo odoo 4096 Jul  2 14:06 app1
drwxr-xr-x 7 odoo odoo 4096 Jul  2 14:09 app2
```

**Alternatively, use privileged permissions each time you run the commands:**

**Locally:**

```sh
sudo mkdir extra-addons/app1
```

**Inside Container:**

```sh
docker exec -it -u root odoo_app odoo scaffold app2 /mnt/extra-addons
```

#### 5. Access the Docker Containers

Once your container is up and running, you can open a bash shell inside the container using:

```sh
docker exec -it odoo_app bash
docker exec -it postgres_db bash
```

#### In Case You Run Into Problems, You Can Have a Fresh Start(Remove container, network and volume)

```sh
docker-compose down -v
```

---