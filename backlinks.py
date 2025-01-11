"""
Process all files in `_posts/` and configure their matching backlinks
"""

import os
import re

blog_base = "https://benjamin-vencill.github.io/jekyll/update"
backlink_regex = r'\[\[(.*?)\]\]'

def name_to_backlink(name: str) -> str:
    """
    Given a post filename, produce it's backlink title.
    """
    return name.split(".")[0].split("-")[-1]

def name_to_url(name: str) -> str:
    """
    Given a post filename, produce it's blog url.
    """
    path = "/".join(name.split("-"))
    path = path.replace(" ", "-")
    path = path.replace(".markdown", ".html")
    return f"{blog_base}/{path}"

valid_backlinks = {name_to_backlink(name): name_to_url(name) for name in os.listdir("_raw")}

print(f"Found {len(valid_backlinks.keys())} backlinks:")
print("".join([f"{key}:{value}" for key, value in valid_backlinks.items()]))

for post in os.listdir("_raw"):
    with open(f"_raw/{post}", "r") as f:
        corpus = f.read()

    backlinks_in_corpus = re.findall(backlink_regex, corpus)
    print(backlinks_in_corpus)
    for backlink in backlinks_in_corpus:
        if backlink in valid_backlinks.keys():
            target = f"[[{backlink}]]"
            payload = f"[{backlink}]({valid_backlinks.get(backlink)})"
            print(f"Replacing {target} with {payload}")
            corpus = corpus.replace(target, payload)
    
    post = post.replace(".md", ".markdown")
    with open(f"_posts/{post}", "w") as f:
        f.write(corpus)

