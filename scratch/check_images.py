import os
import re

html_path = r'd:\My data\Applying\portfolio\portfolio.html'
carousel_dir = r'd:\My data\Applying\portfolio\testimonial photos\carousels'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all src in testimonial photos/carousels
# Use a regex that handles percent encoding
matches = re.findall(r'src="testimonial%20photos/carousels/([^"]+)"', content)

missing = []
for match in matches:
    # URL decode
    filename = match.replace('%20', ' ')
    filepath = os.path.join(carousel_dir, filename)
    if not os.path.exists(filepath):
        missing.append((filename, match))

print("Missing files found in HTML:")
for m in missing:
    print(f"- {m[0]} (src: {m[1]})")

print("\nFiles in directory NOT in HTML:")
files_in_dir = os.listdir(carousel_dir)
matches_decoded = [m.replace('%20', ' ') for m in matches]
count = 0
for f in files_in_dir:
    if f not in matches_decoded:
        print(f"- {f}")
        count += 1
print(f"Total files in dir not in HTML: {count}")
