TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

all: test coverage

coverage: .coverage
	coverage report --fail-under=80

coveralls: .coverage
	coveralls

test:
	flake8 src
	py.test

.PHONY: all coverage coveralls test

###

.coverage: $(TEST) $(SRC)
	coverage run setup.py test

