#!/bin/bash
# Not sure which one of these two is faster:
# curl https://github.com/HackTricks-wiki/hacktricks/archive/refs/heads/master.zip -o master.zip

if [[ -d hacktricks ]]; then
    echo "[*] Updating hacktricks"
    git -C hacktricks pull
else
    echo "[*] Downloading hacktricks from scratch. This may take a couple minutes (depending in your internet speed)"
    git clone https://github.com/HackTricks-wiki/hacktricks.git
fi

# Use venv if it exists
if [[ -d venv ]]; then
    echo "[*] Using python venv"
    source venv/bin/activate
fi

mkdocs build
# python3 -m http.server -d site
