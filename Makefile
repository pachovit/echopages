test:
	pytest -s tests

coverage:
	pytest --cov=echopages -s tests 
