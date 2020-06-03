#!/usr/bin/env bash
mkdir public
python3 manage.py test tenant  manager common | tee public/test.txt
coverage run manage.py test tenant manager common
coverage report | tee public/code_coverage.txt
exit 0