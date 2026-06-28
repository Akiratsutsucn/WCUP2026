with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix all escaped single quotes within JS strings
# The problematic pattern: \' inside JavaScript that should be just '
import re

# The specific line we need to fix contains: opts += \'<option
# Replace all instances of \' that appear inside JavaScript code
html = html.replace("opts += \\'<option", "opts += '<option")
html = html.replace("</option>\\'", "</option>'")

# Also check for any other escaped quotes issues
count = html.count("\\'")
print(f"Remaining backslash-quotes: {count}")

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Fixed")
