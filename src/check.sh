#!/bin/bash

# Fail fast
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"

mypy --strict ${REPO_ROOT}/src/*.py
pytest ${REPO_ROOT}/src
