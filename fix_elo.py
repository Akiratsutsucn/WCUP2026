with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'r', encoding='utf-8') as f:
    e = f.read()

# Only uppercase Elo appears in display strings, variable names use lowercase elo
e = e.replace('Elo', '实力')

with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'w', encoding='utf-8') as f:
    f.write(e)
print('Done - all Elo -> 实力 in engine')
