# Hacktricks Without Ads

This repository contains scripts to deploy / host your own copy of the awesome [book.hacktricks.xyz](https://book.hacktricks.xyz/) website.
It takes the code from <https://github.com/HackTricks-wiki/hacktricks> and builds a website using MkDocs.
My MkDocs config uses custom hooks, that remove advertisements before the page is built.
Since the markup used is not 100% compatible with MkDocs, there are some graphical errors in the resulting page.

<!-- Also added is a search function (@TODO). -->

## Usage

You can find a version hosted by Vercal at TBD.

To build it yourself:

1. Clone this repository:
    ```bash
    git clone https://github.com/six-two/hacktricks-without-ads
    cd hacktricks-without-ads
    ```
2. Clone hacktricks into my repository (to `hacktricks-without-ads/hacktricks`):
    ```bash
    git clone https://github.com/HackTricks-wiki/hacktricks
    ```

    Alternatively you can also download the ZIP file from hacktricks' GitHub site, unzip it and rename it to `hacktricks`.
    But that way you need to redownload everything if you just want to get an updated version of hacktricks.
3. Optional: Set up a python virtual environment:
    ```bash
    python3 -m venv --clear --upgrade-deps venv
    source venv/bin/activate
    ```
4. Install the python dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Run mkdocs to preview the site at <http://127.0.0.1:8000/>:
    ```bash
    mkdocs serve
    ```

    Or to build it to `site/`, you can run:
    ```bash
    mkdocs build
    ```

## Why

Because the ads get in the way too much.
The [enshittification](https://en.wikipedia.org/wiki/Enshittification) is so bad that even the `LICENSE.md` file in their repository has four huge ad images you need to scroll past.
Since the wiki is open source, under a license which I interpret as allowing this type of site (I make no profit and thus am non-commercial), and I already use MkDocs a lot, I decided to try this little project.
