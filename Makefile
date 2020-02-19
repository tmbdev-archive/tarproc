#!/bin/bash

tests: venv
	rm -f objio.yaml objio.yml
	. ./venv/bin/activate; python3 -m pytest -v -x

coverage: venv
	rm -f objio.yaml objio.yml
	. ./venv/bin/activate; coverage run -m pytest -v -x

venv: FORCE
	test -d venv || python3 -m venv venv
	. ./venv/bin/activate; python3 -m pip install --no-cache -r requirements.txt

docs: FORCE
	mkdir -p docs
	cp README.md docs/index.md
	. ./venv/bin/activate; pydocmd simple tarproclib.reader+ | sed 's/:param /- /' > docs/gopen.md
	. ./venv/bin/activate; pydocmd simple tarproclib.writer+ | sed 's/:param /- /' > docs/writer.md
	. ./venv/bin/activate; pydocmd simple tarproclib.zcom+ | sed 's/:param /- /' > docs/zcom.md
	#mv examples/*.md docs
	#./cmd2md obj > docs/obj.md
	#mkdocs build

push: FORCE
	make tests
	make docs
	git add docs/*.md
	git commit -a
	git push

install: FORCE
	sudo python3 -m pip install -r requirements.txt
	sudo python3 setup.py install

clean: FORCE
	rm -rf venv

FORCE:
