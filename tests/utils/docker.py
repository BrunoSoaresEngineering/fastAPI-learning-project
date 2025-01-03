import os
import time

import docker


def is_container_ready(container):
    container.reload()
    return container.status == "running"


def wait_for_stable_status(container, stable_duration=3, interval=1):
    start_time = time.time()
    stable_count = 0

    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= stable_duration / interval:
            return True

        time.sleep(interval)

    return False


def start_database_container():
    client = docker.from_env()
    container_name = "test-db"
    scripts_dir = os.path.abspath("./scripts")

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
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
        "network_mode": "fastapi-development_dev-network",
    }

    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(1)

    if not wait_for_stable_status(container):
        raise RuntimeError("Container did not stabilize within the specified time")

    return container
