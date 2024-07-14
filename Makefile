test:
	PYTHONPATH=. pytest -s tests
	mypy .

coverage:
	PYTHONPATH=. pytest --cov=echopages -s tests
	mypy .

run:
	PYTHONPATH=. python3 echopages/main.py
