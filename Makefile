#!/usr/bin/make -f

build:
	uv run mkdocs build

serve:
	uv run mkdocs serve
