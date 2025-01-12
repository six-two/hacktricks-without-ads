#!/bin/bash
# Not sure which one of these two is faster:
# curl https://github.com/HackTricks-wiki/hacktricks/archive/refs/heads/master.zip -o master.zip

# Change into the project root
cd -- "$( dirname -- "${BASH_SOURCE[0]}" )"

# Install python dependencies
# If you created a virtual python environment, source it
if [[ -f venv/bin/activate ]]; then
    echo "[*] Using virtual python environment"
    source venv/bin/activate
fi

python3 -m pip install -r requirements.txt

# Install/update hacktricks
if [[ -d hacktricks ]]; then
    echo "[*] Updating hacktricks"
    git -C hacktricks pull
else
    echo "[*] Downloading hacktricks from scratch. This may take a couple minutes (depending in your internet speed)"
    git clone https://github.com/HackTricks-wiki/hacktricks.git
fi


# Actually build the site
python3 -m mkdocs build

# Serve the site, if a port was specified as an argument
if [[ -z "$1" ]]; then
    echo "[*] To view the site run:"
    echo python3 -m http.server --directory "'$PWD/site/'"
else
    python3 -m http.server --directory site/ "$1"
fi
