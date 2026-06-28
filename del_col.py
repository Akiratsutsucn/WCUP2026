with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Remove the "球员" header column
h = h.replace('<th style="padding:6px 8px;text-align:right;color:#7aa4c8;">球员</th>', '')

# Remove the data cell for player_count
h = h.replace("(t.player_count || '26') + '/26'", "''")
# Also fix the surrounding td
import re
h = re.sub(r"<td style='padding:5px 8px;text-align:right;'>''</td>", '', h)

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Column removed')
