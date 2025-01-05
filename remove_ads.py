#!/usr/bin/python3
import re
# pip
try:
    from mkdocs.plugins import event_priority
except Exception:
    print("[-] Failed to load event_priority function")

    # Create empty wrapper
    def event_priority(fn, *args, **kwargs):
        return fn

def re_escape(text: str) -> str:
    # re.escape also escapes characters like '-', which should not be escaped.
    # Since all my inputs are static, I can write a simple function myself that should handle all edge cases correctly
    for char in "().":
        text = text.replace(char, "\\" + char)
    return text

def create_sponsor_ad_regex(image_name: str, domain: str) -> re.Pattern:
    pattern_start = f'(<figure>)?<img src="[^"]*?{re_escape(image_name)}[^"]*"'
    # '.' does not match newlines. So to match any character we match everything except the end of a string ('$')
    # Scratch that, with re.DOTALL it should work
    any_substring_shortest_choice = ".*?"
    pattern_end = '{% embed url="[^"]*?' + re_escape(domain) + '.*? %}'
    return re.compile(pattern_start + any_substring_shortest_choice + pattern_end, re.MULTILINE | re.DOTALL)

REMOVE_REGEX_LIST = [
    # Match the Learn AWS hacking banner at the top of all pages
    re.compile(r'\{% hint style="success" %}.{1,10}Learn &.*?\{% endhint %}', re.MULTILINE | re.DOTALL),
    # Special case for pentesting-web/ssti-server-side-template-injection/README.md, where there is a weird malformed link there
    re.compile(r'\{% hint style="success" %}.{1,10}\[https://[^\]]*\]\([^\)]*\)Learn &.*?\{% endhint %}', re.MULTILINE | re.DOTALL),
    # Remove the ads for a lot of the sponsors
    create_sponsor_ad_regex("/pentest-tools.svg", "pentest-tools.com"),
    create_sponsor_ad_regex("/image (48).png", "trickest.com"),
    create_sponsor_ad_regex("/image (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1) (1).png", "stmcyber.com"),
    create_sponsor_ad_regex("https://files.gitbook.com/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-L_2uGJGU7AVNRcqRvEi%2Fuploads%2FelPCTwoecVdnsfjxCZtN%2Fimage.png", "rootedcon.com"),
    create_sponsor_ad_regex("/image (641).png", "rootedcon.com"),
    create_sponsor_ad_regex("/i3.png", "intigriti.com"),
    # Hackenproof does not have the embed link at the end, but instead `**Join us on** [**Discord**](https://discord.com/invite/N3FrSbmwdy) and start collaborating with top hackers today!`
    re.compile(f'<figure><img src="[^"]*?{re_escape("/image (3).png")}[^"]*".*?{re_escape("N3FrSbmwdy) and start collaborating with top hackers today!")}', re.MULTILINE | re.DOTALL),
    # Animated ads are the worst:
    create_sponsor_ad_regex("/RENDER_WebSec_10fps_21sec_9MB_29042024.gif", "websec.nl"),

    # There are different hacktricks training banners?
    re.compile(r'\{\{#include .*/banners/hacktricks-training.md}}'),
]
REPLACE_AD_WITH = "\n\n[AD REMOVED]\n\n"
regex_use_counter: dict[re.Pattern, int] = {}

### MkDocs Plugin

def on_pre_build(config) -> None:
    reset_counters()

@event_priority(70) # run this before all other plugins
def on_page_markdown(markdown: str, page, config, files) -> str:
    return remove_ads(markdown)

def on_post_build(config) -> None:
    print_counters()

### End: MkDocs Plugin

def remove_ads(markdown: str) -> str:
    old_markdown = markdown
    for regex in REMOVE_REGEX_LIST:
        markdown = regex.sub(REPLACE_AD_WITH, markdown)
        if markdown != old_markdown:
            old_markdown = markdown
            regex_use_counter[regex] = regex_use_counter.get(regex, 0) + 1

    return markdown

def reset_counters() -> None:
    # Reset all counters, should not be necessary but is here as a sanity measure
    for key in list(regex_use_counter.keys()):
        del regex_use_counter[key]
    
    # Explicitely store all entries with zero, so that we can iterate over them
    for regex in REMOVE_REGEX_LIST:
        regex_use_counter[regex] = 0

def print_counters() -> None:
    # Print regexes sorted by frequency with the most important ones at the top
    print("\n\n=== Regex statistics ===")
    for regex, count in sorted(regex_use_counter.items(), key=lambda x: x[1], reverse=True):
        print(f"Regex {regex.pattern} used on {count} pages")
    print("===\n\n")


if __name__ == "__main__":
    import argparse
    import os

    ap = argparse.ArgumentParser(description="Call this directly to check how many regexes match without actually building the full site with mkdocs")
    ap.add_argument("path_to_hacktricks", help="the path to the hacktricks folder")
    args = ap.parse_args()

    reset_counters()

    for dirpath, dirnames, filenames in os.walk(args.path_to_hacktricks):
        for file_name in filenames:
            if file_name.endswith(".md"):
                file_path = os.path.join(dirpath, file_name)
                try:
                    with open(file_path, "r") as f:
                        # This will increment the counters if patterns match
                        remove_ads(f.read())
                except Exception as e:
                    print(f"[-] Failed to read {file_path} due to error: {e}")

    print_counters()
