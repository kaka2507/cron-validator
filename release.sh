#!/usr/bin/env bash
pip install -r requirements/release.txt
python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
