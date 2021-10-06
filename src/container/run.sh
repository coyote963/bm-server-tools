#!/bin/bash
export DISPLAY=:1.0
/startup.sh &
sleep 15 && flask run --port=8000 --host=0.0.0.0