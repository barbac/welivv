.PHONY: init all migrate test server clean

PIP_LOG := build/pip.log
CSV := testdata/50k_businesses.csv

init: build $(PIP_LOG) migrate server

all: build $(PIP_LOG) migrate build/load_data test server

build:
	mkdir -p $@

$(PIP_LOG): requirements.txt
	pip install -r $< | tee $(PIP_LOG)

#this one could look for the model files and save the migrate log to avoid running migrate.
migrate:
	./manage.py migrate

db.sqlite3: migrate

build/load_data: $(CSV)
	./manage.py load_data testdata/50k_businesses.csv
	touch $@

test:
	py.test -v businesses/*

server:
	./manage.py runserver

clean:
	rm -f build/load_data
	rm -f $(PIP_LOG)
