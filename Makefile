test:
	PYTHONPATH=src pytest src/tests

unit_test:
	PYTHONPATH=src pytest src/tests/unit_tests.py

perf_test:
	PYTHONPATH=src pytest src/tests/perf_tests.py

coverage:
	-coverage run -m pytest
	-coverage report -m
	-coverage html

lint:
	ruff check

doc:
	pdoc3 --html --output-dir docs/ src/app