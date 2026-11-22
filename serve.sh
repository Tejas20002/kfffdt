#!/bin/sh
# Serve both versions at http://localhost:8080  (chooser page at /)
cd "$(dirname "$0")" && python3 -m http.server 8080
