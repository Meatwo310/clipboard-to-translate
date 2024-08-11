#!/bin/bash

set -euo pipefail

if [ ! -d .venv ]; then
    echo "# Creating virtual environment"
    python3 -m venv .venv
fi

echo "# Installing requirements"
.venv/bin/pip3 install -r requirements.txt

echo "Done! You can now run the script with: .venv/bin/python3 main.py"
