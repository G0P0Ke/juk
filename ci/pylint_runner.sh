#!/usr/bin/env bash
mkdir public
pylint manage.py common juk manager tenant | tee public/pylint.txt
exit 0
