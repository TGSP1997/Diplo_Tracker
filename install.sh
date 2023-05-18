#!/bin/bash
set -e
#Set Working Directory
WORKING_DIR=$(pwd)

#Install Venv
if [ ! -d "$WORKING_DIR"/venv ]; then
  python -m venv venv
fi


#Requierements of ExtRepros
source "$WORKING_DIR"/venv/Scripts/activate
python -m pip install cmake==3.26.3
python -m pip install -r "$WORKING_DIR"/requirements.txt
deactivate
