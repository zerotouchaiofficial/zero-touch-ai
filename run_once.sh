#!/bin/bash
set -e

python generate.py
python voice.py
python video.py
python upload.py

