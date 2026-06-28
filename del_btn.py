with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Find and remove the button
h = h.replace('<button class="btn-sm" onclick="loadMysticDetail()">查看详情</button>', '')

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Button removed')
