with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Remove all flag emojis from the FLAGS JS object - set all values to empty string
import re
# Match pattern: 'CountryName':'flag_emoji' and replace flag with empty
h = re.sub(r"':'[^\']*'", "':''", h)  # Only within FLAGS definition, but this is too broad

# Better: find FLAGS = { ... } and clear all values
start = h.find('var FLAGS = {')
end = h.find('};', start) + 2
if start > 0 and end > start:
    flags_block = h[start:end]
    # Replace all flag emoji values with empty string
    cleaned = re.sub(r":'[^']+'", ":''", flags_block)
    h = h[:start] + cleaned + h[end:]

# Fix getFlag fallback
h = h.replace("return FLAGS[team] || '\U0001f30d'", "return ''")
h = h.replace("return FLAGS[team] || '🌍'", "return ''")
h = h.replace("return FLAGS[team] || ''", "return ''")

# Also remove flag spans from display (they use getFlag which now returns '')
# But keep the function call for compatibility

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Flags cleared from FLAGS object')
