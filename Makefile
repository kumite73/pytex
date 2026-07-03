# Makefile
.PHONY: lint test test-api test-cov test-api-cov test-api doc build clean
run:
	python -m app

lint:
	pre-commit run --all-files

test:
	pytest tests -s

clean:
	python -c "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"

test-cov:
	pytest tests --cov=. --cov-config=tests/.coveragerc --cov-report html

doc:
	pdoc -o docs -d google --no-show-source app

.ONESHELL:
build:
	docker build -t pytex:local .
