#!/bin/bash
set -e
#Set Working Directory
WORKING_DIR=$(pwd)

#Install Venv
if [ ! -d "$WORKING_DIR"/.venv ]; then
  python -m venv .venv
fi

#Repros
if [ ! -d "$WORKING_DIR"/ExtRepros/OTVision ]; then
  git clone https://github.com/OpenTrafficCam/OTVision.git "$WORKING_DIR"/ExtRepros/OTVision
fi
if [ ! -d "$WORKING_DIR"/ExtRepros/OTAnalytics ]; then
  git clone https://github.com/OpenTrafficCam/OTAnalytics.git "$WORKING_DIR"/ExtRepros/OTAnalytics
fi

#Requierements of ExtRepros
source "$WORKING_DIR"/.venv/Scripts/activate
python -m pip install --upgrade -r "$WORKING_DIR"/ExtRepros/OTVision/requirements.txt
python -m pip install --upgrade -r "$WORKING_DIR"/ExtRepros/OTAnalytics/requirements.txt
deactivate
