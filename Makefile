PYTHON ?= python3

.PHONY: start build full check docker

start:
	./start.sh

build:
	$(PYTHON) tools/build.py

full:
	$(PYTHON) tools/slides.py
	$(PYTHON) tools/build.py
	$(PYTHON) tools/check.py

check:
	$(PYTHON) tools/check.py

docker:
	docker compose up --build
