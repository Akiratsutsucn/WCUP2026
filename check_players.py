import json
d = json.load(open('/root/wcup2026/data/wc2026_players_processed.json'))
teams = d.get('teams', d)
print('teams type:', type(teams).__name__)
if isinstance(teams, dict):
    tkeys = list(teams.keys())
    print('Team count:', len(tkeys))
    print('Sample:', tkeys[:10])
    first = teams[tkeys[0]]
    print('First team type:', type(first).__name__)
    if isinstance(first, dict):
        print('Keys:', list(first.keys())[:8])
        if 'players' in first:
            print('Player count:', len(first['players']))
            p = first['players'][0]
            print('Player:', p.get('name'), p.get('age'), p.get('caps'))
    elif isinstance(first, list) and len(first) > 0:
        print('Player count:', len(first))
        p = first[0]
        print('Player keys:', list(p.keys())[:10])
