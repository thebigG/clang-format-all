.PHONY: clean lint build deploy virtual-env activate-virtual-env

deploy: build
		pip install twine
		twine upload -r pypi dist/*

virtual-env:
	virtualenv -p python3 venv

clean:
	rm -r build

build-src:
	pip install .

build:
	pip install build
	python3 -m build
