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



# apply_migrations() {
#     echo "Applying database migrations..."
#     alembic upgrade head
#     echo "Migrations completed"
# }

# create_initial_data() {
#     echo "Checking and creating initial data..."
#     python -c "
# from database import SessionLocal
# from models import Category
# db = SessionLocal()
# if not db.query(Category).first():
#     initial_categories = [
#         Category(name='Restaurant', description='Places to eat'),
#         Category(name='Park', description='Public spaces and parks'),
#         Category(name='Museum', description='Cultural institutions'),
#         Category(name='Hotel', description='Places to stay')
#     ]
#     db.bulk_save_objects(initial_categories)
#     db.commit()
# db.close()
#     "
#     echo "Initial data check completed"
# }

# if [ -z "${POSTGRES_USER}" ] || [ -z "${POSTGRES_PASSWORD}" ] || [ -z "${POSTGRES_DB}" ]; then
#     echo "Error: Missing required environment variables"
#     exit 1
# fi

wait_for_postgres

# apply_migrations

# create_initial_data

echo "Starting application..."
gunicorn main:app \
    --bind 0.0.0.0:8080 \
    --workers ${WORKERS:-4} \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout 120 \
    --keep-alive 5 \
    --log-level ${LOG_LEVEL:-info} \
    --access-logfile - \
    --error-logfile - \
    --reload
