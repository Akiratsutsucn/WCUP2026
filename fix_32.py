with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'r', encoding='utf-8') as f:
    e = f.read()

# Fix get_rankings to filter to R32 teams
old = "results.sort(key=lambda x: x[\"adjusted_prob\"], reverse=True)\n        return results"
new = """results.sort(key=lambda x: x["adjusted_prob"], reverse=True)
        r32_teams = _get_r32_teams()
        if r32_teams:
            results = [r for r in results if r["team"] in r32_teams]
        return results"""
e = e.replace(old, new)

# Add helper function
helper = '''
def _get_r32_teams():
    try:
        matches = _load_json("matches.json")
        teams = set()
        for m in matches.get("matches", []):
            if m.get("round") == "R32":
                if m.get("home"): teams.add(m["home"])
                if m.get("away"): teams.add(m["away"])
        return teams
    except:
        return None
'''
idx = e.find('class PredictionEngine:')
if idx > 0:
    e = e[:idx] + helper + '\n' + e[idx:]

with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'w', encoding='utf-8') as f:
    f.write(e)

# Fix frontend
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()
h = h.replace('球队评分因子构成（全部排名）', '球队评分因子构成（32强排名）')
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Done')
