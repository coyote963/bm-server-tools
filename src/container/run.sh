#!/bin/bash

# Necessary for ASCII encoding error: 
# https://stackoverflow.com/questions/36651680/click-will-abort-further-execution-because-python-3-was-configured-to-use-ascii
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_ENV=development
cd server
flask run --port=8000 --host=0.0.0.0