all: install test README.md

install: $(shell find groupbyrule -type f) pypackage.toml setup.cfg
	pip install -e .

test: $(shell find groupbyrule -type f) pypackage.toml setup.cfg
	pytest --doctest-modules

README.md: README.ipynb $(shell find groupbyrule -type f)
	jupyter nbconvert --to markdown README.ipynb
