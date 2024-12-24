import re

# '.' does not match newlines. So to match any character we match everything except the end of a string ('$')
ANY_CHAR_INCLUDING_LINE_BREAK = "[^$]"

REMOVE_REGEX_LIST = [
    # Match the Learn AWS hacking banner at the top of all pages
    re.compile(r'\{% hint style="success" %}[^$]{1,10}Learn &[^$]*?\{% endhint %}', re.MULTILINE),
    # Remove the inline embeds with ads for pentest-tools
    re.compile(r'<figure><img src="/\.gitbook/assets/pentest-tools\.svg"[^$]*?{% embed url="https://pentest-tools\.com.*? %}', re.MULTILINE),
]
REPLACE_AD_WITH = "\n\n[AD REMOVED]\n\n"
regex_use_counter: dict[re.Pattern, int] = {}

def on_pre_build(config) -> None:
    # Reset all counters, should not be necessary but is here as a sanity measure
    for key in list(regex_use_counter.keys()):
        del regex_use_counter[key]
    
    # Explicitely store all entries with zero, so that we can iterate over them
    for regex in REMOVE_REGEX_LIST:
        regex_use_counter[regex] = 0

def on_page_markdown(markdown: str, page, config, files) -> str:
    return remove_ads(markdown)

def on_post_build(config) -> None:
    # Show how many pages matched each regex (multiple matches on a page are counted only once)
    # Useful to debug regexes and see whether they match anything at all

    # Print regexes sorted by frequency with the most important ones at the top
    print("\n\n=== Regex statistics ===")
    for regex, count in sorted(regex_use_counter.items(), key=lambda x: x[1], reverse=True):
        print(f"Regex {regex.pattern} used on {count} pages")
    print("===\n\n")

def remove_ads(markdown: str) -> str:
    old_markdown = markdown
    for regex in REMOVE_REGEX_LIST:
        markdown = regex.sub(REPLACE_AD_WITH, markdown)
        if markdown != old_markdown:
            old_markdown = markdown
            regex_use_counter[regex] = regex_use_counter.get(regex, 0) + 1

    return markdown

