#!/usr/bin/env bash

pylint manage.py common juk manager tenant | tee public/pylint.txt
exit 0
