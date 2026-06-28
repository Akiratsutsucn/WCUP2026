import json
d = json.load(open('/root/wcup2026/data/wc2026_players_processed.json'))
teams = d.get('teams', {})
# Check US/Mexico/Brazil
for name in ['United States', 'USA', 'Mexico', 'Brazil', 'Argentina']:
    if name in teams:
        t = teams[name]
        pl = t.get('players', [])
        print(f'{name}: {len(pl)} players, ages sample: {[p.get(\"age\") for p in pl[:3]]}')
    else:
        print(f'{name}: NOT FOUND')
print()
print('Available team keys:', list(teams.keys()))
