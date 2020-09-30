---
title: "Docker Nodejs Postgresql Example"
date: 2020-06-06T00:01:13+02:00
draft: true
toc: false
description: summary of blogpost
author: loeken
summary: a demo of how to run 2 containers in the same virtual network using docker and docker-compose with a nodejs/postgresql application - code provided on github repository
images:
tags:
  - untagged
---

### example postgresql/nodejs in two containers

<div class="flex">

![](/media/img/docker_postgresql_nodejs.png)

</div>

[Download Image Markup](/media/imgmarkup/docker_example_nodejs_postgresql.py)

first we need to grab the postgresql image

```
docker pull postgres:12
```

```
docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
62e4019570d2        bridge              bridge              local
c1aeefb374e7        host                host                local
608568a867c3        none                null                local
```

```
docker network create testnetwork1 
577e8e0c44c4ca0c0b1d855a70536e875bf77ec0010fdbfaf5db1d131ddabd69

docker network ls
NETWORK ID          NAME                DRIVER              SCOPE
62e4019570d2        bridge              bridge              local
c1aeefb374e7        host                host                local
608568a867c3        none                null                local
577e8e0c44c4        testnetwork1        bridge              local
```
##### docker volumes:
docker containers dont have persistent storage out of the box. you can easily map a folder to the host. this way data will remain after restarts.
so far i've come across 3 ways of how one can specify volumes:
1.) anonymous volumes
example:
```
-v /var/lib/postgresql 
```
this is the easiest syntax, you simply specify the path inside the container and docker will create a volume in /var/lib/docker/volumes ( named via hash )

2.) named volumes
imo the cleanest way: you specify the path within the container and add a name
example:
```
-v postgresql:/var/lib/postgresql
```
this will create a folder inside /var/lib/docker/volumes on the host and name it postgresql

3.) mapped paths
good for quick n easy tests or when you want to specify a specific location on the host to store the data on.
example:
```
-v $PWD/postgresql_data:/var/lib/postgresql
```

##### fire up postgresql
create the container based on the image and forward the postgresql port 
```
docker run -it \
          -p 5432:5432 \
          -e POSTGRES_PASSWORD="topsecure" \
          -e PGDATA=/var/lib/postgresql/data/pgdata \
          --net=testnetwork1 \
          --name=postgresql \
          -v $PWD/docker_nodejs_postgresql_demo/postgresql_data:/var/lib/postgresql/data \
          postgres:12
5bc0816ecac54fef7e334ebd243a5a62c5859c8eeb639cea85414165bb9c7506
```

let's query the logs and see if the startup went fine
```
docker logs postgresql
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.

The database cluster will be initialized with locale "en_US.utf8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".

Data page checksums are disabled.

fixing permissions on existing directory /var/lib/postgresql/data ... ok
creating subdirectories ... ok
selecting dynamic shared memory implementation ... posix
selecting default max_connections ... 100
selecting default shared_buffers ... 128MB
selecting default time zone ... Etc/UTC
creating configuration files ... ok
running bootstrap script ... ok
performing post-bootstrap initialization ... ok
syncing data to disk ... ok
initdb: warning: enabling "trust" authentication for local connections
You can change this by editing pg_hba.conf or using the option -A, or
--auth-local and --auth-host, the next time you run initdb.


Success. You can now start the database server using:

    pg_ctl -D /var/lib/postgresql/data -l logfile start

waiting for server to start....2020-06-06 10:54:05.039 UTC [46] LOG:  starting PostgreSQL 12.3 (Debian 12.3-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
2020-06-06 10:54:05.049 UTC [46] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2020-06-06 10:54:05.073 UTC [47] LOG:  database system was shut down at 2020-06-06 10:54:04 UTC
2020-06-06 10:54:05.079 UTC [46] LOG:  database system is ready to accept connections
 done
server started

/usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*

2020-06-06 10:54:05.125 UTC [46] LOG:  received fast shutdown request
waiting for server to shut down....2020-06-06 10:54:05.127 UTC [46] LOG:  aborting any active transactions
2020-06-06 10:54:05.130 UTC [46] LOG:  background worker "logical replication launcher" (PID 53) exited with exit code 1
2020-06-06 10:54:05.131 UTC [48] LOG:  shutting down
2020-06-06 10:54:05.153 UTC [46] LOG:  database system is shut down
 done
server stopped

PostgreSQL init process complete; ready for start up.

2020-06-06 10:54:05.245 UTC [1] LOG:  starting PostgreSQL 12.3 (Debian 12.3-1.pgdg100+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 8.3.0-6) 8.3.0, 64-bit
2020-06-06 10:54:05.245 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
2020-06-06 10:54:05.245 UTC [1] LOG:  listening on IPv6 address "::", port 5432
2020-06-06 10:54:05.252 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
2020-06-06 10:54:05.275 UTC [55] LOG:  database system was shut down at 2020-06-06 10:54:05 UTC
2020-06-06 10:54:05.281 UTC [1] LOG:  database system is ready to accept connections
```

lets now create a database connect to it and insert sample data 
```
psql -h localhost -U postgres -W
Passwort: 
psql (12.3)
Geben Sie »help« für Hilfe ein.

postgres=# CREATE DATABASE api;
CREATE DATABASE

api=# \c api;
Passwort für Benutzer postgres: 
Sie sind jetzt verbunden mit der Datenbank »api« als Benutzer »postgres«.

api=# \dt
Keine Relationen gefunden

api=# CREATE TABLE users (
              ID SERIAL PRIMARY KEY,
              name VARCHAR(30),
              email VARCHAR(30)
      );
INSERT INTO USERS values (1,'foo','bar');
INSERT 0 1
```

now we can fire up a docker container with example code
```
cd Projects
git clone https://github.com/loeken/docker_nodejs_postgresql_demo
cd docker_nodejs_postgresql_demo
```
we download the example project which is a very basic app that connects to postgresql, reads and prints records.
```
const pg = require('pg');

const cs = 'postgres://postgres:topsecure@postgresql:5432/api';

const client = new pg.Client(cs);
client.connect();

client.query('SELECT * FROM users').then(res => {

    const data = res.rows;

    console.log('all data');
    data.forEach(row => {
        console.log(`Id: ${row.id} Name: ${row.name} Email: ${row.email}`);
    })
}).finally(() => {
    client.end()
});
```
and now let's start up  our application:
```
docker run -it \
           --rm \
           --name docker_nodejs_postgresql_demo \
           --net=testnetwork1 \
           -v "$PWD/index.js":/usr/src/app/index.js \
           localhost:5000/docker_nodejs_postgresql_demo
all data
Id: 1 Name: Foo Email: foo@bar.com
```

#### docker compose
a unified way to combine the run commands for various containers into a single file. you will need docker-compose installed for this to work.

and we ll use the image that we created in the [last blobpost](/posts/docker-create-images-in-a-private-self-hosted-registry/)
#### **`docker-compose.yml`**
``` 
version: '3'
services:
  postgresql:
    image: postgres:12
    ports:
      - 5432:5432
    environment:
      - POSTGRES_PASSWORD="topsecure"
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - /home/loeken/Projects/docker_nodejs_postgresql_demo/postgresql_data:/var/lib/postgresql/data
  docker_nodejs_postgresql_demo:
    image: localhost:5000/docker_nodejs_postgresql_demo
    depends_on:
      - postgresql
    volumes: 
      - /home/loeken/Projects/docker_nodejs_postgresql_demo/index.js:/usr/src/app/index.js
```

as we already have the start command defined within the Dockerfile we can remove the command: directive here.
<style type="text/css">
.flex { 
    display: flex; 
    justify-content: center; 
    align-items: center;
}
</style>