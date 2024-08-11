PORT:=3000
PYTHONPATH=./
CONFIG_PATH=./deploy/config.toml

run:
	CONFIG_PATH=./deploy/config.toml poetry run uvicorn src.main:app --host localhost --port $(PORT) --factory

run_all:
	docker compose up minio keycloak kc_postgres postgres --build -d
	poetry run uvicorn src.main:app --host localhost --port $(PORT) --factory

migrations_init:
	alembic revision --autogenerate -m "init"

makemigrations:
	alembic revision --autogenerate -m "$(MSG)"

migrate:
	alembic upgrade head

migrate_with_data:
	alembic -x data=true upgrade head

downgrade:
	alembic downgrade -1

test_long:
	pytest --maxfail=1 --cov=app -vv --cov-config .coveragerc

test:
	pytest --maxfail=1 --cov=app -vv --cov-config .coveragerc -m "not long"

lint:
	pre-commit run --all-files
