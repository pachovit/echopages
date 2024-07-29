test:
	PYTHONPATH=. pytest -s tests
	pre-commit run --all-files

functional:
	PYTHONPATH=. pytest -s tests/functional
	
coverage:
	PYTHONPATH=. pytest --cov=echopages -s tests
	pre-commit run --all-files

run:
	PYTHONPATH=. python3 echopages/main.py
