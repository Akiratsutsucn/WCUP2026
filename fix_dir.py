p = 'E:/Workspace/Kun/WCUP2026/prediction/engine.py'
with open(p, 'r', encoding='utf-8') as f: h = f.read()
h = h.replace("'compute_all_mystic' in dir()", "'compute_all_mystic' in globals()")
h = h.replace("'compute_team_mystic' in dir()", "'compute_team_mystic' in globals()")
h = h.replace("'compute_ucl_signals' in dir()", "'compute_ucl_signals' in globals()")
with open(p, 'w', encoding='utf-8') as f: f.write(h)
print('Fixed')
