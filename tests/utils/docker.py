import os

import docker


def start_database_container():
    client = docker.from_env()
    container_name = "test-db"

    try:
        existing_container = client.containers.get(container_name)
        print(f"Container '{container_name} exists. Stopping and removing...")
        existing_container.stop()
        existing_container.remove()
        print(f"Container '{container_name} stopped and removed")
    except docker.errors.NotFound:
        print(f"Container '{container_name} does not exist.")

    container_config = {
        "name": container_name,
        "image": "postgres:alpine",
        "detach": True,
        "ports": {"5432": "5434"},
        "environment": {
            "POSTGRES_USER": os.getenv("POSTGRES_TEST_USER"),
            "POSTGRES_PASSWORD": os.getenv("POSTGRES_TEST_PASSWORD"),
        },
    }

    container = client.containers.run(**container_config)
