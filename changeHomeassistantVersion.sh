#!/bin/bash
[[ -z "$1" ]] && { echo "Please supply current version"; exit 1; }
[[ -z "$2" ]] && { echo "Please supply target version"; exit 1; }
sed -i 's/'"$1"'/'"$2"'/g' docker-compose.yaml
sed -i 's/'"$1"'/'"$2"'/g' .github/workflows/homeassistant-installed.yaml
sed -i 's/'"$1"'/'"$2"'/g' README.md
sed -i 's/'"$1"'/'"$2"'/g' www/plantuml/homeassistant-architecture.puml
