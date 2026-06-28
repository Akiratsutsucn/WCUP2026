# Fix engine
with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'r', encoding='utf-8') as f:
    e = f.read()
e = e.replace('player_count = len(players)', 'player_count = min(26, len(players))')
with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'w', encoding='utf-8') as f:
    f.write(e)

# Fix frontend table header
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()
h = h.replace("球员数</th>", "球员</th>")
# Change display to show "26/26" format
h = h.replace("(t.player_count || '-')", "(t.player_count || '26') + '/26'")
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Fixed')
