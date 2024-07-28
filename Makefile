test:
	PYTHONPATH=. pytest -s tests
	mypy . --strict

functional:
	PYTHONPATH=. pytest -s tests/functional
	
coverage:
	PYTHONPATH=. pytest --cov=echopages -s tests
	mypy . --strict

run:
	PYTHONPATH=. python3 echopages/main.py
