#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER project_db_usr WITH PASSWORD 'project_db_pwd';
    CREATE DATABASE project_db WITH OWNER project_db_usr;
    GRANT ALL PRIVILEGES ON DATABASE project_db TO project_db_usr;
EOSQL
