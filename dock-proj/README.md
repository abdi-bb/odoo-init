# Development Guidelines for Odoo Inside Docker

## 0. Begin

```sh
mkdir proj-dir
cd proj-dir
```

## 1. Write the `docker-compose.yaml` file

Create a file named `docker-compose.yaml` and add the following content:

```yaml
version: '3.1'

services:
  db:
    image: postgres:13
    container_name: postgres_db
    restart: always
    ports:
      - "5444:5432"
    environment:
      # Create db superuser inside `postgres` db
      - POSTGRES_USER=test_usr
      - POSTGRES_PASSWORD=test_pwd
      - POSTGRES_DB=postgres
    # env_file: .env
    volumes:
      - db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:15.0
    container_name: odoo_app
    ports:
      - "8069:8069"
    environment:
      # Connect to db, using the above created user
      - HOST=db
      - PORT=5432
      - USER=test_usr
      - PASSWORD=test_pwd
    # env_file: .env
    volumes:
      - web-data:/var/lib/odoo
      - ./extra-addons:/mnt/extra-addons
    depends_on:
      - db
    command: ["-i", "base", "-d", "test_db"]

volumes:
  db-data:
  web-data:
```

## 2. Run Docker Compose

Build and start the containers with the following command:

```sh
docker-compose up --build --remove-orphans
# Because of the mount inside docker compose file this command will create `extra-addons` dir inside `proj-dir`
```

## 3. Adjust the Ownership of `extra-addons` Directory(The step matters: First do inside docker container)

To allow both local and Docker editing of the `extra-addons` directory, adjust its ownership and permissions:

Change the ownership of the `extra-addons` directory inside the Docker container:

```sh
docker exec -it -u root odoo chown -R odoo:odoo /mnt/extra-addons
```

Change the ownership of the `extra-addons` directory on your local machine:

```sh
sudo chown -R $USER:odoo extra-addons
sudo chmod -R 775 extra-addons
```

If you encounter an error, ensure you have the `odoo` group:

```sh
sudo groupadd odoo
sudo usermod -aG odoo $USER
```

## 4. Confirm Permissions

Check the permissions of the `extra-addons` directory locally and inside the Docker container:

### Local Directory

```sh
mkdir extra-addons/app1 # Now should work without permission error
ls -l extra-addons
# Sample output
❯ ls -l extra-addons                   
total 4
drwxrwxr-x 2 abdi odoo 4096 Jul  1 12:14 app1
```

### Docker Container Directory

```sh
docker exec -it odoo ls -l /mnt/extra-addons
# Sample output
 ❯ docker exec -it odoo_app ls -l /mnt/extra-addons
total 4
drwxrwxr-x 2 1000 1001 4096 Jul  1 09:14 app1

```

## 5. Access the Docker Container

Once your container is up and running, you can open a bash shell inside the container using:

```sh
docker exec -it odoo bash
```