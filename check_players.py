import json
d = json.load(open('/root/wcup2026/data/wc2026_players_processed.json'))
teams = d.get('teams', {})
for name in ['Brazil', 'Argentina', 'France']:
    if name in teams:
        pl = teams[name].get('players', [])
        if pl:
            p = pl[0]
            print(name, 'keys:', sorted(p.keys()))
            print('  name:', p.get('name'))
            for cn_key in ['name_cn', 'name_zh', 'chinese_name', 'cn_name']:
                if cn_key in p:
                    print(f'  {cn_key}:', p[cn_key])
        else:
            print(name, 'no players')
    else:
        print(name, 'NOT FOUND')
