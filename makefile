all: README.md dist

README.md: README.ipynb $(shell find groupbyrule -type f)
	jupyter nbconvert --to markdown README.ipynb

dist: $(shell find groupbyrule -type f) pypackage.toml setup.cfg
	python3 -m build