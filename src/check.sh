#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

mypy --strict ${SCRIPT_DIR}/*.py
pytest ${SCRIPT_DIR}
