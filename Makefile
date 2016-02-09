.PHONY: all test coverage coveralls flake8 dist clean

all:	flake8 test coverage

test:
	py.test -v -s

coverage:
	coverage run --source land -m py.test && coverage report

coveralls:
	py.test --cov land tests/ --cov-report=term --cov-report=html

flake8:
	flake8 land tests manage.py

server:
	./run.sh

load:
	bin/loader.py

init:
	pip3 install -r requirements/dev.txt

upgrade:
	pip3 install --upgrade -r requirements/dev.txt

clean:
	-find . -name "*.pyc" | xargs rm -f
	-find . -name "__pycache__" | xargs rm -rf
	-rm -rf dist
	-rm -rf build
