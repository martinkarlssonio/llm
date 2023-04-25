#!/bin/bash
#Set up virtual environment
cd src
pip3 install virtualenv
mkdir llm-venv
python3 -m venv llm-venv/env
source llm-venv/env/bin/activate && pip install -r requirements.txt
python3 app.py