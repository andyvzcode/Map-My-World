#!/bin/bash
set -e

wait_for_postgres() {
    echo "Waiting for PostgreSQL to start..."
    while ! pg_isready -h "${SERVICE_NAME_DB}" -p "${POSTGRES_PORT}" -U "${POSTGRES_USER}" >/dev/null 2>&1; do
        echo "Waiting for PostgreSQL..."
        sleep 2
    done
    echo "PostgreSQL started successfully"
}


wait_for_postgres


echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
