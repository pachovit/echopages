test:
	PYTHONPATH=. pytest -s tests

coverage:
	PYTHONPATH=. pytest --cov=echopages -s tests 

run:
	PYTHONPATH=. python3 echopages/main.py
