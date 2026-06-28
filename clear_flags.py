import re
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find FLAGS object and clear ALL values  
start = h.find('var FLAGS = {')
end = h.find('};', start) + 2
if start > 0 and end > start:
    flags_block = h[start:end]
    # Replace all values with empty string
    cleaned = re.sub(r":'[^']*'", ":''", flags_block)
    h = h[:start] + cleaned + h[end:]

# Force getFlag to always return empty
h = h.replace("function getFlag(team){ return FLAGS[team] || ''; }", "function getFlag(team){ return ''; }")

# Also strip any remaining complex flag emoji sequences from the file
# (England's flag uses multiple codepoints)
for flag in ['\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f',
             '\U0001f3f4']:
    while flag in h:
        h = h.replace(flag, '')

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('All flags cleared')
