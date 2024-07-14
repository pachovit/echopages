test:
	PYTHONPATH=. pytest -s tests

coverage:
	PYTHONPATH=. pytest --cov=echopages -s tests 
