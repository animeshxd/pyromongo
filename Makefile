setup:
	pip install -r requirements.txt
	pip install setuptools wheel twine

install:
	python setup.py install

install_dev:
	pip install -e .

build:
	git stash --include-untracked
	python setup.py sdist bdist_wheel
	git stash pop

upload: build
	twine upload dist/*

clean:
	rm build/ dist/ *.egg-info -rf
