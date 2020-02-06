PIP_LOG := build/pip.log

init: build $(PIP_LOG)
	./manage.py migrate

build:
	mkdir -p $@

$(PIP_LOG): requirements.txt
	pip install -r $< | tee $(PIP_LOG)
