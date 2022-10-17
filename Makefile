test:
	docker run --rm --name="java-tron"\
		-v /Users/pomeschenkoanton/projects/tronql/data/testnet/node:/java-tron/output-directory \
		-v /Users/pomeschenkoanton/projects/tronql/data/testnet/logs:/java-tron/logs \
		-p 8090:8090 -p 18888:18888 -p 50051:50051 \
		java-tron -c /java-tron/config/test_net_config.conf

build_test:
	docker build -t java-tron -f nile/Dockerfile nile

build_app:
	docker build -t tronql app

build_router:
	docker build -t router -f app/Dockerfile.router app

prod:
	docker run --rm --name="java-tron" \
		-v /Users/pomeschenkoanton/projects/tronql/data/mainnet/node:/java-tron/output-directory \
		-v /Users/pomeschenkoanton/projects/tronql/data/mainnet/logs:/java-tron/logs \
		-p 8090:8090 -p 18888:18888 -p 50051:50051 \
		tronprotocol/java-tron:GreatVoyage-v4.5.2 -c /java-tron/config/test_net_config.conf --es

reset:
	rm -rf data/kafka/config
	rm -rf data/kafka/data
	rm -rf data/testnet/logs/tron.log
	rm -rf data/testnet/node/database
	rm -rf data/testnet/node/index
	rm -rf data/zookeeper/data
