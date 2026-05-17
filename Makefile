ROOT_DIR=$(shell pwd)
APP_DIR=$(ROOT_DIR)/src/app
export PYTHONPATH=$(APP_DIR)

dev:
	uv run uvicorn src.app.main:app --port 8080 --reload

init:
	uv sync

build:
	uv run src/app/build.py

view:
	uv run uvicorn src.app.view:app --port 8090