run:
	docker run -it -p 9090:9090 --rm --name tron tronbox/tre

test:
	tronbox test

compile:
	tronbox compile

deploy_market:
	tronbox compile
	set -o allexport; source .env; set +o allexport; . .venv/bin/activate; python deploy.py Market
	cp ./artifacts/Market.json ../src/src/abis/Market.json
