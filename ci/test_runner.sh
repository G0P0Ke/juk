#!/usr/bin/env bash

python3 manage.py test manager common | tee public/test.txt
coverage run manage.py test manager common 
coverage report | tee public/code_coverage.txt
exit 0