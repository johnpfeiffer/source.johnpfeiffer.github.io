#!/bin/bash
# at the same location as pelican.conf 
make clean; pelican content; cd output/ ; python -m SimpleHTTPServer
