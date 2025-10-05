import openai
import os
import json
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")
if openai.api_key is None:
    raise ValueError("OPENAI_API_KEY not set. Export it as an environment variable.")

# Prompt user
title = input("Enter blog title/topic: ")
extra = input("Enter extra details about topic here: ")

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that writes blog posts."},
        {"role": "user", "content": f"Write a blog post titled '{title}' with a short 1-sentence summary at the top. Please make sure to use these details in the post: {extra}"}
    ],
    temperature=0.7
)

content_raw = response['choices'][0]['message']['content']
paragraphs = content_raw.split('\n')
summary = paragraphs[0].strip()
content = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs[1:] if p.strip())

# File setup
slug = title.lower().replace(" ", "-").replace("/", "-")
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"posts/blog_{slug}_{date_str}.html"
link = filename

# Write HTML
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Christina Jordan</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; background-color: #f0e7d9; color: #3b2918; }}
        a {{ text-decoration: none; color: #5f3c10; }} a:hover {{ text-decoration: underline; }}
        header {{ background-color: #726048; color: #f0e7d9; text-align: center; padding: 60px 20px; }}
        header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
        header p {{ font-size: 1.2rem; color: #ddd5c8; }}
        nav {{ background-color: #5a4c39; display: flex; justify-content: center; flex-wrap: wrap; }}
        nav a {{ padding: 15px 25px; color: #f0e7d9; font-weight: bold; transition: background 0.3s; }}
        nav a:hover {{ background-color: #575757; }}
        section {{ max-width: 1000px; margin: 50px auto; padding: 0 20px; }}
        h2 {{ text-align: center; margin-bottom: 30px; font-size: 2rem; }}
        p {{ margin-bottom: 1rem; }}
        footer {{ text-align: center; padding: 30px 20px; background-color: #726048; color: white; }}
    </style>
</head>
<body>

<header>
    <h1>Christina Jordan</h1>
    <p>Chemical & Biomolecular Engineering @ Georgia Tech</p>
</header>

<nav>
    <a href="index.html#about">About Me</a>
    <a href="index.html#projects">Projects</a>
    <a href="index.html#community">Community</a>
    <a href="blog.html">Blog</a>
    <a href="index.html#resume">Résumé</a>
    <a href="index.html#contact">Contact</a>
</nav>

<section>
    <h2>{title}</h2>
    {content}
</section>

<footer>
    <p>&copy; 2025 Christina Jordan</p>
</footer>

</body>
</html>"""

# Save HTML
with open(filename, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Blog saved to {filename}")

# --- Update blog-posts.json ---
post_data = {
    "title": title,
    "excerpt": summary,
    "link": link,
    "date": date_str
}

json_file = "blog-posts.json"
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = []

data.insert(0, post_data)  # newest first

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("blog-posts.json updated.")
