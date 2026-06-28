import re
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Remove the susp tab button (with any spacing variations)
h = re.sub(r'<button class="nav-btn" data-tab="susp">\s*伤病停赛\s*</button>\s*', '', h)
# Remove the case from switch
h = re.sub(r"case 'susp':\s*html = renderSuspensions\(\);\s*break;\s*", '', h)

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Removed')
