with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find the specific broken line and fix it
# Current: svg += '<g onclick="openModal(' + mid + '')" style="cursor:pointer">';
# Target:  svg += '<g onclick="openModal(\'' + mid + '\')" style="cursor:pointer">';

old = "svg += '<g onclick=\"openModal(' + mid + '')\" style=\"cursor:pointer\">';"
new = "svg += '<g onclick=\"openModal(\\'' + mid + '\\')\" style=\"cursor:pointer\">';"

if old in h:
    h = h.replace(old, new)
    print('Fixed onclick')
else:
    print('Pattern not found, searching...')
    # Search for similar pattern
    idx = h.find('svg += <g onclick=')
    if idx > 0:
        print('Found at', idx, ':', h[idx:idx+100])

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
