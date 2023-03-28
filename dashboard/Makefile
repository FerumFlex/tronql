### alembic
revision:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; alembic revision --autogenerate -m $(filter-out $@,$(MAKECMDGOALS))

upgrade:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; alembic upgrade head

downgrade:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; alembic downgrade -1

history:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; alembic history

# servers
projects_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; uvicorn --reload projects.main:app --port 4102 --host 0.0.0.0

auth_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; uvicorn --reload auth.main:app --port 4101 --host 0.0.0.0

token_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; uvicorn --reload projects.auth:app --port 5100 --host 0.0.0.0

stats_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; uvicorn --reload stats.main:app --port 4103 --host 0.0.0.0

stats_worker:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; python3 -m stats.worker

# graphql apollo
compose:
	rover supergraph compose --config ./supergraph.yaml > supergraph-schema.graphql

run:
	APOLLO_GRAPH_REF=1 ../bin/router --dev --config router.yaml --supergraph supergraph-schema.graphql --hot-reload --apollo-uplink-poll-interval 10s --anonymous-telemetry-disabled --apollo-uplink-endpoints projects --apollo-uplink-timeout 5s
