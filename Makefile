test:
	PYTHONPATH=src pytest src/tests

unit_test:
	PYTHONPATH=src pytest src/tests/unit_test.py

perf_test:
	PYTHONPATH=src pytest src/tests/perf_test.py

coverage:
	-coverage run -m pytest
	-coverage report -m
	-coverage html

lint:
	ruff check

doc:
	pdoc3 --html --force --output-dir docs/ src/app