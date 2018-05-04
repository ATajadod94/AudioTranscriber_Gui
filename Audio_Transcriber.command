#!/bin/sh
here="`dirname \"$0\"`"
cd "$here" || exit 1
cd ./Scripts/Google_Transcribtion
python3 Audio_Transcriber.py