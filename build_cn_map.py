import json

# Load CN team names from team_names_cn.json
with open('E:/Workspace/Kun/WCUP2026/data/team_names_cn.json', 'r', encoding='utf-8') as f:
    en_to_cn = json.load(f)

# Load Chinese players from zh wiki  
with open('E:/Workspace/Kun/WCUP2026/data/cn_players.json', 'r', encoding='utf-8') as f:
    cn_teams_players = json.load(f)

# Build reverse mapping: Chinese team name → English team name
cn_to_en = {v: k for k, v in en_to_cn.items()}

# Build final mapping: English team name → [Chinese player names]
en_players_cn = {}
matched = 0
for cn_team, players in cn_teams_players.items():
    en_team = cn_to_en.get(cn_team, cn_team)
    en_players_cn[en_team] = players
    matched += 1

print(f"Matched {matched}/{len(cn_teams_players)} teams")
for en, pl in list(en_players_cn.items())[:5]:
    print(f"  {en} ({en_to_cn.get(en, '?')}): {pl[:3]}")

# Save combined file
with open('E:/Workspace/Kun/WCUP2026/data/cn_players_en.json', 'w', encoding='utf-8') as f:
    json.dump(en_players_cn, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(en_players_cn)} teams with {sum(len(p) for p in en_players_cn.values())} players")
