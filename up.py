import os
import socket
import subprocess
import yaml

# Load configuration from YAML file
with open('portconfig.yml', 'r') as f:
    config = yaml.safe_load(f)

# Load existing Docker Compose configuration
with open('docker-compose.yml', 'r') as f:
    docker_compose_config = yaml.safe_load(f)

for service in config['services']:
    SERVICE_NAME = service['service']
    HOST_PORT = service['host_port']
    CONTAINER_PORT = service['container_port']

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_in_use = sock.connect_ex(('localhost', HOST_PORT)) == 0
    sock.close()

    if port_in_use:
        print(f"Port {HOST_PORT} is already in use. Using only container port.")
        ports = f'{CONTAINER_PORT}'
    else:
        print(f"Port {HOST_PORT} is available.")
        ports = f'{HOST_PORT}:{CONTAINER_PORT}'

    # Update Docker Compose configuration in memory
    docker_compose_config['services'][SERVICE_NAME]['ports'] = [f'{ports}']

# Create temporary Docker Compose file
with open('docker-compose-temp.yml', 'w') as f:
    yaml.safe_dump(docker_compose_config, f)

# Start Docker services
subprocess.run(["docker", "compose", "-f", "docker-compose-temp.yml", "up", "-d"])

for service in config['services']:
    SERVICE_NAME = service['service']
    CONTAINER_PORT = service['container_port']
    
    output = subprocess.check_output(["docker", "compose", "port", SERVICE_NAME, str(CONTAINER_PORT)])
    allocated_port = output.decode('utf-8').split(':')[1].strip()
    print(f"Service {SERVICE_NAME} was allocated port {allocated_port} on the host machine")

# Delete temporary Docker Compose file
os.remove('docker-compose-temp.yml')
