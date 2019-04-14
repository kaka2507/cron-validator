#!/usr/bin/env bash
pip install -r requirements/release.txt
python setup.py sdist
twine upload dist/*
