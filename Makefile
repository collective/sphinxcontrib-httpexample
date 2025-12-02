help:
	@grep -Eh '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' | uniq

SPHINX ?= 8.3.2
PYTHON ?= python39

.PHONY: clean
clean:  ## Clean up build artifacts
	rm -rf devenv.local.nix

.PHONY: docs
docs:  ## Build docs
	PYTHONPATH=$(PWD)/docs sphinx-build -b html docs docs/html

.PHONY: format
format:  ## Format code
	treefmt

.PHONY: watch
watch:  ## Watch build docs
	PYTHONPATH=$(PWD)/docs sphinx-autobuild -b html docs docs/html

.PHONY: show
show:  ## Show installed packages
	@python --version
	@python -c "from importlib import metadata; print('\n'.join(sorted(d.metadata['Name'] + f' {d.version}' for d in metadata.distributions() if d.metadata['Name'].lower() in ['docutils', 'sphinx'])))"

.PHONY: test
test: ## Run tests
	PYTHONPATH=$(PWD)/docs pytest --cov sphinxcontrib.httpexample tests

.PHONY: devenv-%
devenv-%: devenv.local.nix
	devenv shell $(MAKE) $*

shell: devenv.local.nix  ## Start a shell with the development environment
	devenv shell

###

htmlcov: .coverage
	coverage html

coverage.xml: .coverage
	coverage xml

coverage: coverage.xml

.PHONY: test\ all
test\ all:  ## Test all supported versions
	make PYTHON=python314 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python314 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python314 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python314 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python313 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python312 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=8.2.3 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python311 SPHINX=7.4.7 clean devenv-show devenv-test
	make PYTHON=python310 SPHINX=8.1.3 clean devenv-show devenv-test
	make PYTHON=python310 SPHINX=8.0.2 clean devenv-show devenv-test
	make PYTHON=python310 SPHINX=7.4.7 clean devenv-show devenv-test

devenv.local.nix:
	@echo '{ pkgs, ...}: { languages.python = { interpreter = pkgs.$(PYTHON); dependencies = [ "sphinx$(subst .,,$(SPHINX))" "dev" ]; }; }' > devenv.local.nix
