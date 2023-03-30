#!/bin/bash
set -e
WORKING_DIR=$(pwd)

git clone https://github.com/OpenTrafficCam/OTVision.git "$WORKING_DIR"/OpenTrafficCam/OTVision
git clone https://github.com/OpenTrafficCam/OTAnalytics.git "$WORKING_DIR"/OpenTrafficCam/OTAnalytics

