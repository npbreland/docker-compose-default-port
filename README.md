# Docker Compose Default Port

I made this tiny script beacuse I was annoyed that Docker Compose would fail to bring up a service if the port on the host machine was already blocked. 
This script (which you can alias to `docker compose up` or whatever you prefer), will read from a `portconfig.yml` file in your current directory, which should have the following structure:

```yaml
services:
  - service: laravel.test
    host_port: 80
    container_port: 80
  - service: mysql
    host_port: 3306
    container_port: 3306
```

You don't need to specify every service! if you don't want to one of your services to be treated this way, just leave it out of the `portconfig.yml`

The script will attempt to bind each specified service to its specified `host_port` on the host machine, but if it fails, it will allow Compose to dynamically allocate the port, 
which Compose already does when the host_port is not specified in the docker-compose.yml file. It will then print which ports were allocated:

```
Service laravel.test was allocated port 32775 on the host machine
Service mysql was allocated port 32774 on the host machine
```

Have fun!
