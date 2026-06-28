with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Remove onclick from bracket SVG matches
h = h.replace(
    "svg += '<g onclick=\"openModal(\\'' + mid + '\\')\" style=\"cursor:pointer\">';",
    "svg += '<g>';"
)

# Also remove the cursor:pointer style 
h = h.replace(' style="cursor:pointer"', '')

# Remove the bracket editing buttons
h = h.replace(
    "h += '<div class=\"btn-bar\"><button class=\"btn-sm\" onclick=\"fillR32()\">自动填充32强</button><button class=\"btn-sm\" onclick=\"resetBracket()\" style=\"background:#5a3030;color:#e88;\">重置全部比赛</button></div>';",
    "h += '';"
)

# Remove the modal HTML and related JS
# Keep modal for potential future use but remove editing capability from bracket

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Edit removed, dates should show')
