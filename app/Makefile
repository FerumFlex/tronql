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
blocks_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; strawberry server --port 3100 blocks.main

blocks_worker:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; faust -A blocks.faust --datadir data/block-data worker --web-port 6000

trans_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; strawberry server --port 3101 trans.main

trans_worker:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; faust -A trans.faust --datadir data/transaction-data worker --web-port 6001

node_web:
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; strawberry server --port 3102 node.main

# graphql apollo
compose:
	rover supergraph compose --config ./supergraph.yaml > supergraph-schema.graphql

run:
	./router --dev --config router.yaml --supergraph supergraph-schema.graphql --hot-reload --apollo-uplink-endpoints 60
