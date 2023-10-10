#!/bin/bash
python3 -m pip install requests
python3 -m pip install unicodedata
python3 -m pip install lxml

python3 YouTubeLinkGrabber.py > ./youtube.m3u8

echo M3U update complete.
