import json
from zhconv import convert

# Load Chinese player data
with open('E:/Workspace/Kun/WCUP2026/data/cn_players_en.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert all player names to Simplified Chinese
total = 0
for team, players in data.items():
    for i in range(len(players)):
        old = players[i]
        new = convert(old, 'zh-cn')
        if old != new:
            players[i] = new
            total += 1

# Save
with open('E:/Workspace/Kun/WCUP2026/data/cn_players_en.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Converted {total} names to Simplified Chinese")
# Show samples
for team in ['Brazil', 'Argentina', 'Uruguay']:
    if team in data:
        print(f"  {team}: {data[team][:3]}")

# Also convert team_names_cn.json
with open('E:/Workspace/Kun/WCUP2026/data/team_names_cn.json', 'r', encoding='utf-8') as f:
    cn_names = json.load(f)

for k, v in cn_names.items():
    cn_names[k] = convert(v, 'zh-cn')

with open('E:/Workspace/Kun/WCUP2026/data/team_names_cn.json', 'w', encoding='utf-8') as f:
    json.dump(cn_names, f, ensure_ascii=False, indent=2)
print("\nTeam names also converted")
