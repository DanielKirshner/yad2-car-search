#!/bin/bash

echo 'Prepering Environment...'

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

echo 'Done!!!'
