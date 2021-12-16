#!/bin/bash

# Fail fast
set -e
REPO_ROOT="$(git rev-parse --show-toplevel)"

NEW_DAY=$1
echo $NEW_DAY
cp ${REPO_ROOT}/src/d2.py ${REPO_ROOT}/src/${NEW_DAY}.py
touch ${REPO_ROOT}/input/${NEW_DAY}
touch ${REPO_ROOT}/input/${NEW_DAY}-example
code ${REPO_ROOT}/src/${NEW_DAY}.py
code ${REPO_ROOT}/input/${NEW_DAY}
code ${REPO_ROOT}/input/${NEW_DAY}-example
echo "#${NEW_DAY}p1p2 ${NEW_DAY}-example (0, 0)" >> ${REPO_ROOT}/answers
echo "#${NEW_DAY}p1p2 ${NEW_DAY} (0, 0)" >> ${REPO_ROOT}/answers


git add ${REPO_ROOT}/src/${NEW_DAY}.py ${REPO_ROOT}/input/${NEW_DAY} ${REPO_ROOT}/input/${NEW_DAY}-example