#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $DIR
git pull
git log -1 --oneline > currentCommit.txt
./turnBarRed.sh > /dev/null
./restartHomeassistant.sh > /dev/null
#docker restart homeassistant
