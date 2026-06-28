import json, math

# Load group stage data
with open('E:/Workspace/Kun/WCUP2026/data/standings.json', 'r', encoding='utf-8') as f:
    standings = json.load(f)

# Compute league-wide averages
all_teams = []
for g in standings.values():
    for t in g:
        all_teams.append(t)

avg_gf = sum(t['gf'] for t in all_teams) / len(all_teams)
avg_ga = sum(t['ga'] for t in all_teams) / len(all_teams)
print(f"Average GF: {avg_gf:.2f}, Average GA: {avg_ga:.2f}")

# Build team profiles
profiles = {}
for g in standings.values():
    for t in g:
        name = t['team']
        attack = t['gf'] / avg_gf if avg_gf > 0 else 1.0      # >1 = above avg attack
        defense = t['ga'] / avg_ga if avg_ga > 0 else 1.0      # <1 = better defense (conceded less)
        pts_per_game = t['pts'] / t['p'] if t['p'] > 0 else 0
        gd_per_game = t['gd'] / t['p'] if t['p'] > 0 else 0
        profiles[name] = {
            'attack': round(attack, 2),
            'defense': round(defense, 2),
            'pts_per_game': round(pts_per_game, 2),
            'gd_per_game': round(gd_per_game, 2),
            'gf': t['gf'],
            'ga': t['ga'],
            'pts': t['pts'],
            'gd': t['gd']
        }

# Also load Elo data
with open('E:/Workspace/Kun/WCUP2026/data/elo_cache_2026.json', 'r', encoding='utf-8') as f:
    elo_cache = json.load(f)

# Print some profiles
for team in ['France', 'Brazil', 'Argentina', 'Norway', 'Cape Verde', 'DR Congo']:
    if team in profiles:
        p = profiles[team]
        elo = elo_cache.get(team, 1700)
        if isinstance(elo, dict): elo = elo.get('elo', 1700)
        print(f"  {team}: GF={p['gf']} GA={p['ga']} GD={p['gd']} Pts={p['pts']}  Attack={p['attack']} Defense={p['defense']} Elo={elo:.0f}")

# Save profiles
with open('E:/Workspace/Kun/WCUP2026/data/team_profiles.json', 'w', encoding='utf-8') as f:
    json.dump(profiles, f, indent=2, ensure_ascii=False)
print(f"\nSaved {len(profiles)} team profiles")
