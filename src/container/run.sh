#!/bin/bash
mkdir -p /root/.config/BoringManRewrite
# Start the flask server
flask run
# Call the startup script of the vnc server
/bin/bash /startup.sh
