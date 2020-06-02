#!/bin/bash

cd docs
export PYTHONPATH=..
make html
cd ..
mv docs/_build/html public/docs