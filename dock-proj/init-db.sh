#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER test_usr WITH PASSWORD 'test_usr_pwd';
    CREATE DATABASE project_db WITH OWNER test_usr;
    GRANT ALL PRIVILEGES ON DATABASE project_db TO test_usr;
EOSQL
