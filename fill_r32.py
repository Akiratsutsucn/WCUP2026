import json

with open('E:/Workspace/Kun/WCUP2026/data/matches.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# R32 matchups from user - all 16 matches
r32 = [
    ("M1",  "South Africa", "Canada"),
    ("M2",  "Brazil", "Japan"),
    ("M3",  "Germany", "Paraguay"),
    ("M4",  "Netherlands", "Morocco"),
    ("M5",  "Ivory Coast", "Norway"),
    ("M6",  "France", "Sweden"),
    ("M7",  "Mexico", "Ecuador"),
    ("M8",  "England", "DR Congo"),
    ("M9",  "Belgium", "Senegal"),
    ("M10", "United States", "Bosnia and Herzegovina"),
    ("M11", "Spain", "Austria"),
    ("M12", "Portugal", "Croatia"),
    ("M13", "Switzerland", "Algeria"),
    ("M14", "Australia", "Egypt"),
    ("M15", "Argentina", "Cape Verde"),
    ("M16", "Colombia", "Ghana"),
]

for mid, home, away in r32:
    for m in data['matches']:
        if m['id'] == mid:
            m['home'] = home
            m['away'] = away
            m['home_score'] = None
            m['away_score'] = None
            m['winner'] = None
            print(f"Set {mid}: {home} vs {away}")

with open('E:/Workspace/Kun/WCUP2026/data/matches.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nDone! All 16 R32 matches populated.")
