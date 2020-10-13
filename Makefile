.PHONY: run-production
run-production: setup-prod
	FLASK_ENV=production FLASK_APP=app/app.py flask run

.PHONY: run-development
run-development: setup-dev
	FLASK_ENV=development FLASK_APP=app/app.py flask run

.PHONY: test
test: setup-dev
	py.test -v

.PHONY: setup-dev
setup-dev:
	pip install -r requirements/dev.txt

.PHONY: setup-prod
setup-prod:
	pip install -r requirements/prod.txt

.PHONY: env
env:
	python3 -m venv .env
