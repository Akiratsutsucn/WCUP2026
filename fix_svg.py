with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

h = h.replace('var maxY = 25 + 15*GAP_Y + BOX_H + 30;', 'var maxY = 25 + 15*GAP_Y + BOX_H + 40;')
# Fix date text Y position - render date inside the gap between boxes
h = h.replace("(p.y+BOX_H+10)", "(p.y+BOX_H+14)")
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Fixed')
