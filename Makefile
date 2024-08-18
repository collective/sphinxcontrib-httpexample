export PYTHON ?= python27
export FEATURE ?= docutils016

TEST = $(wildcard tests/*.py)
SRC = $(wildcard src/sphinxcontrib/httpexample/*.py)

.PHONY: all
all: test coverage

.PHONY: docs
docs:
	sphinx-build -b html docs docs/html
ifeq "$(PYTHON)" "python27"
	sphinx-build -b pdf docs docs/pdf
endif

.PHONY: coverage
coverage: .coverage
	coverage report --fail-under=80

.PHONY: coveralls
coveralls: .coverage
	coveralls --service=github

.PHONY: format
format:
	black --skip-string-normalization src tests

.PHONY: nix-fmt
nix-fmt:
	nix fmt flake.nix setup.nix

.PHONY: show
show:
	pip freeze

.PHONY: test
test:
	flake8 src
	py.test

###

.PHONY: nix-%
nix-%:
	nix develop .#$(PYTHON)-$(FEATURE) --accept-flake-config --command $(MAKE) $*

.PHONY: nix-shell
nix-shell:
	nix develop .#$(PYTHON)-$(FEATURE) --accept-flake-config

.PHONY: shell
shell:
	nix develop .#$(PYTHON)-$(FEATURE) --accept-flake-config

env:
	nix build .#$(PYTHON)$-(FEATURE)-env --accept-flake-config -o env

.cache:
	mkdir -p .cache
	if [ -d ~/.cache/pip ]; then ln -s ~/.cache/pip ./.cache; fi

.coverage: $(TEST) $(SRC)
	coverage run setup.py test

nix/requirements-python27.nix: .cache nix/requirements-python27.txt
	nix develop .#python27-pip2nix --command pip2nix generate -r nix/requirements-python27.txt --output=nix/requirements-python27.nix

nix/requirements-python27.txt: .cache requirements.txt
	nix develop .#python27-pip2nix --command pip2nix generate -r requirements.txt --output=nix/requirements-python27.nix
	@grep "pname =\|version =" nix/requirements-python27.nix|awk "ORS=NR%2?FS:RS"|sed 's|.*"\(.*\)";.*version = "\(.*\)".*|\1==\2|' > nix/requirements-python27.txt

poetry\ add\ --dev\ %:
	cp nix/poetry-$(PYTHON)-$(FEATURE).toml pyproject.toml
	cp nix/poetry-$(PYTHON)-$(FEATURE).lock poetry.lock
	poetry add --group dev $*
	mv pyproject.toml nix/poetry-$(PYTHON)-$(FEATURE).toml
	mv poetry.lock nix/poetry-$(PYTHON)-$(FEATURE).lock

every\ poetry\ add\ --dev\ %:
	 PYTHON=python39  FEATURE=docutils018 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python39  FEATURE=docutils019 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python39  FEATURE=docutils020 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python310 FEATURE=docutils018 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python310 FEATURE=docutils019 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python310 FEATURE=docutils020 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python311 FEATURE=docutils018 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python311 FEATURE=docutils019 $(MAKE) poetry\ add\ --dev\ $*
	 PYTHON=python311 FEATURE=docutils020 $(MAKE) poetry\ add\ --dev\ $*
