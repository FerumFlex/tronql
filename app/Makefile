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
node_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; uvicorn --reload node.main:app --port 3102 --host 0.0.0.0

# graphql apollo
compose:
	rover supergraph compose --config ./supergraph.yaml > supergraph-schema.graphql

run:
	APOLLO_GRAPH_REF=1 ../bin/router --dev --config router.yaml --supergraph supergraph-schema.graphql --hot-reload --apollo-uplink-endpoints 60
