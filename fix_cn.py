import re
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

reps = [
    (r"t\.team \+ '</span>'", r"cn(t.team) + '</span>'"),
    (r"predictData\.rankings\[i\]\.team \+ '</option>'", r"cn(predictData.rankings[i].team) + '</option>'"),
    (r"d\.team_a \+ '</div><div class=\"elo\">'", r"cn(d.team_a) + '</div><div class=\"elo\">'"),
    (r"d\.team_b \+ '</div><div class=\"elo\">'", r"cn(d.team_b) + '</div><div class=\"elo\">'"),
    (r"d\.team_a \+ ' 获胜'", r"cn(d.team_a) + ' 获胜'"),
    (r"d\.team_b \+ ' 获胜'", r"cn(d.team_b) + ' 获胜'"),
    (r"预期进球：' \+ d\.team_a", r"预期进球：' + cn(d.team_a)"),
    (r"m\.home\|\|'待定'", r"cn(m.home||'待定')"),
    (r"m\.away\|\|'待定'", r"cn(m.away||'待定')"),
    (r"' ' \+ team \+ '</b><br>'", r"' ' + cn(team) + '</b><br>'"),
    (r"' ' \+ team \+ '</span><span>'", r"' ' + cn(team) + '</span><span>'"),
    (r"t\.team \+ '</td>'", r"cn(t.team) + '</td>'"),
]

total = 0
for old, new in reps:
    html, n = re.subn(old, new, html)
    if n > 0:
        total += n
        print(f"OK ({n}x): {old[:60]}")

# Also fix the H2H draw label which shows team name
html = re.sub(r"d\.team_b \+ '</div>'", r"cn(d.team_b) + '</div>'", html)

# Fix the bracket match card display - team name in span
html = re.sub(r"\(m\.home\|\|'待定'\)", r"(cn(m.home||'待定'))", html)
html = re.sub(r"\(m\.away\|\|'待定'\)", r"(cn(m.away||'待定'))", html)

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\nTotal: {total} replacements")
