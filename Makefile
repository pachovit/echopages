test:
	PYTHONPATH=. pytest -s tests
	pre-commit run --all-files

functional:
	PYTHONPATH=. pytest -s tests/functional
	
coverage:
	PYTHONPATH=. pytest --cov=echopages -s tests
	pre-commit run --all-files

run:
	docker compose --env-file .env -f simple.docker-compose.yml up -d --build

build-frontend:
	cd echopages/frontend && npm install && npm run build && cd ../../