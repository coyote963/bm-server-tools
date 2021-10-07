#!/bin/bash
export DISPLAY=:1.0
export HOME=/root
/startup.sh &
sleep 10 && flask run --port=8000 --host=0.0.0.0