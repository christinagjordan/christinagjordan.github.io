from google import genai
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

# Initialize client using the environment variable GEMINI_API_KEY
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Use standard library logging/error handling instead of print
    raise ValueError("GEMINI_API_KEY environment variable not set. Please ensure it is in your .env file.")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

def get_input_with_validation(prompt_text):
    """Utility to get non-empty input from the user."""
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

print("\n--- Blog Post Content Generator ---\n")
title = get_input_with_validation("Enter blog title/topic: ")
extra = input("Enter extra details about topic (optional): ").strip()

print("\nGenerating content with Gemini...\n")

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        # Requesting a specific format to aid in parsing: title, summary, then body
        contents=f"Write a complete blog post titled '{title}' on this topic. "
                 f"Start the response with the full blog post title on its own line. "
                 f"The second line must be a short 1-sentence summary followed by a blank line. "
                 f"Ensure paragraphs are separated by double newlines. "
                 f"Include these specific details: {extra}"
    )
except Exception as e:
    print(f"An error occurred during content generation: {e}")
    exit(1)

# Extract generated content
content_raw = response.text

# Split content based on the expected structure
lines = content_raw.split('\n')
# The model should provide the Title and Summary in the first two lines
generated_title_raw = lines[0].strip() if lines else ""
summary = lines[1].strip() if len(lines) > 1 else ""

# The rest of the content is treated as the body
body_content = '\n'.join(lines[2:]).strip()

# Create HTML paragraphs from the body content
paragraphs = body_content.split('\n\n')
content_html = ''.join(f'<p>{p.strip()}</p>' for p in paragraphs if p.strip())

# Simple slug generation: lowercases and replaces spaces/slashes with hyphens
slug = title.lower().replace(" ", "-").replace("/", "-")
slug = ''.join(c for c in slug if c.isalnum() or c == '-')
date_str = datetime.now().strftime("%Y-%m-%d")
os.makedirs("posts", exist_ok=True)
filename = f"posts/blog_{slug}_{date_str}.html"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Christina Jordan</title>
    <style>
        /* Modern, earth-tone aesthetic */
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.7; background-color: #fcf8f3; color: #3b2918; }}
        a {{ text-decoration: none; color: #5f3c10; transition: color 0.3s; }} a:hover {{ text-decoration: underline; color: #8c5d2c; }}
        header {{ background-color: #726048; color: #fcf8f3; text-align: center; padding: 60px 20px; }}
        header h1 {{ font-size: 2.5rem; margin-bottom: 5px; }}
        header p {{ font-size: 1.2rem; color: #ddd5c8; }}
        nav {{ background-color: #5a4c39; display: flex; justify-content: center; flex-wrap: wrap; border-bottom: 3px solid #726048; }}
        nav a {{ padding: 15px 25px; color: #fcf8f3; font-weight: 500; transition: background 0.3s, color 0.3s; }}
        nav a:hover {{ background-color: #4a3e2f; }}
        .content-container {{ max-width: 800px; margin: 50px auto; padding: 0 25px; }}
        .blog-title {{ font-size: 2.5rem; margin-bottom: 10px; color: #3b2918; text-align: center; font-weight: 700; }}
        .blog-summary {{ font-size: 1.15rem; margin-bottom: 30px; padding: 15px; background-color: #ede2d3; border-left: 5px solid #726048; font-style: italic; color: #5a4c39; border-radius: 4px; }}
        p {{ margin-bottom: 1.2rem; font-size: 1.05rem; text-align: justify; }}
        h2 {{ text-align: center; margin-top: 50px; margin-bottom: 20px; font-size: 1.8rem; color: #5f3c10; }}
        footer {{ text-align: center; padding: 30px 20px; background-color: #726048; color: #fcf8f3; margin-top: 80px; }}
        .contact-icon {{ fill: #5f3c10; transition: fill 0.3s; }}
        .contact-icon:hover {{ fill: #726048; }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
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
    <a href="assets/christina_jordan_resume.pdf">Résumé</a>
    <a href="#contact">Contact</a>
</nav>

<div class="content-container">
    <h1 class="blog-title">{generated_title_raw}</h1>
    <p class="blog-summary">{summary}</p>

    <!-- Blog Content -->
    <section>
        {content_html}
        <!-- Optional: Add a note about the date -->
        <p style="text-align: right; font-size: 0.9em; color: #999;">Published on {date_str}</p>
    </section>

    <!-- Contact -->
    <section id="contact">
        <h2>Contact</h2>
        <div style="text-align:center; display:flex; justify-content:center; gap:40px; flex-wrap:wrap; margin-top:20px;">
            <!-- Email SVG -->
            <a href="mailto:christinagjordan@gmail.com" title="Email">
                <svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
                    <path d="M12 13.5L0 6V18h24V6l-12 7.5zM12 12l12-7H0l12 7z"/>
                </svg>
            </a>
            <!-- LinkedIn SVG -->
            <a href="https://linkedin.com/in/christinagjordan" target="_blank" title="LinkedIn">
                <svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
                    <path d="M19 0h-14c-2.76 0-5 2.24-5 5v14c0 2.76 2.24 5 5 5h14c2.762 0 5-2.238 5-5v-14c0-2.76-2.238-5-5-5zm-11 19h-3v-10h3v10zm-1.5-11.5c-.966 0-1.75-.784-1.75-1.75s.784-1.75 1.75-1.75 1.75.784 1.75 1.75-.784 1.75-1.75 1.75zm13.5 11.5h-3v-5.5c0-1.379-1.121-2.5-2.5-2.5s-2.5 1.121-2.5 2.5v5.5h-3v-10h3v1.421c.844-1.297 2.708-1.844 4.166-1.421 2.059.595 3.334 2.597 3.334 4.999v4.001z"/>
                </svg>
            </a>
            <!-- GitHub SVG -->
            <a href="https://github.com/christinagjordan" target="_blank" title="GitHub">
                <svg class="contact-icon" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
                    <path d="M12 .297c-6.627 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.387.6.111.82-.261.82-.577v-2.234c-3.338.724-4.033-1.415-4.033-1.415-.546-1.387-1.333-1.756-1.333-1.756-1.089-.744.083-.729.083-.729 1.205.084 1.839 1.236 1.839 1.236 1.07 1.834 2.809 1.304 3.495.997.108-.775.418-1.304.762-1.604-2.665-.304-5.466-1.334-5.466-5.931 0-1.309.467-2.381 1.236-3.221-.124-.303-.536-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.655 1.652.243 2.873.12 3.176.77.84 1.234 1.912 1.234 3.221 0 4.609-2.805 5.624-5.475 5.921.43.371.814 1.102.814 2.222v3.293c0 .319.218.694.825.576 4.765-1.589 8.203-6.084 8.203-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
            </a>
        </div>
    </section>
</div>

<footer>
    <p>&copy; {datetime.now().year} Christina Jordan</p>
</footer>

</body>
</html>"""

# Write HTML file
try:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Blog post successfully saved to: {filename}")
except Exception as e:
    print(f"Error writing HTML file: {e}")
    exit(1)

post_data = {
    "title": generated_title_raw, # Use the title generated by the model
    "excerpt": summary,
    "link": f"christinagjordan.github.io/{os.path.basename(filename)}", # Use only the filename for relative link
    "date": date_str
}

json_file = "blog-posts.json"
data = []

# Read existing data if the file exists
if os.path.exists(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read or decode {json_file}. Starting fresh list. Error: {e}")
        data = []

# Insert the new post data at the beginning (newest first)
data.insert(0, post_data)

# Write updated data
try:
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Blog index file updated: {json_file}")
except Exception as e:
    print(f"Error writing JSON file: {e}")

print("\n--- Process Complete ---")