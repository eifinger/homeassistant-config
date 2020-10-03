#!/bin/bash
[[ "$#" -eq "0" ]] && { echo "Please supply target version"; exit 1; }
[[ "$#" -eq "1" ]] && { currentVersion=$(cat .HA_VERSION); targetVersion="$1"; }
[[ "$#" -eq "2" ]] && { currentVersion="$1"; targetVersion="$2"; }
sed -i 's/'"$currentVersion"'/'"$targetVersion"'/g' docker-compose.yaml .github/workflows/homeassistant-installed.yaml README.md www/plantuml/homeassistant-architecture.puml
echo "Changed Homeassistant version from $currentVersion to $targetVersion in all files."
