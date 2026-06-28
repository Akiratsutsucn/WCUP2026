import re

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all non-ASCII characters that look like emoji (skip Chinese/Cyrillic/Arabic etc)
# Emoji ranges: https://en.wikipedia.org/wiki/Emoji#Unicode_blocks
emoji_ranges = [
    (0x1F300, 0x1F9FF),  # Misc Symbols, Emoticons, etc
    (0x2600, 0x27BF),    # Misc symbols
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F680, 0x1F6FF),  # Transport
    (0x1F900, 0x1F9FF),  # Supplemental
    (0x2702, 0x27B0),    # Dingbats
    (0x1F1E0, 0x1F1FF),  # Flags (keep these!)
]

# But DON'T touch flag emojis (U+1F1E0-U+1F1FF)
# And don't touch Chinese characters (U+4E00-U+9FFF)

def is_emoji(cp):
    for lo, hi in emoji_ranges:
        if lo <= cp <= hi:
            return True
    return False

# Also handle specific known emojis
extra_emojis = [
    '⚽', '⚡', '⚠', '✅', '❌', '⬆️', '⬇️', '➖', 
    '🔄', '🏆', '🔬', '⚔', '👥', '🏥', '🏟', '📊', '📅', '📍', '🎯',
    '🤕', '🟨', '🟥', '🌍', '🌊', '🔴', '💧', '🔮', '📈', '📋'
]

count = 0
for e in extra_emojis:
    n = html.count(e)
    if n > 0:
        html = html.replace(e, '')
        count += n

# Also remove emoji from tab buttons and headings
# Replace common emoji patterns in HTML text

print(f"Removed {count} additional emoji instances")

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify - count remaining emojis
remaining = 0
for e in extra_emojis:
    remaining += html.count(e)
print(f"Remaining emoji instances: {remaining}")
