test:
	PYTHONPATH=. pytest -s tests
	mypy . --strict

coverage:
	PYTHONPATH=. pytest --cov=echopages -s tests
	mypy . --strict

run:
	PYTHONPATH=. python3 echopages/main.py
