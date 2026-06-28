import re, json

with open('E:/Workspace/Kun/WCUP2026/zh_squads.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all sortable tables
tables = list(re.finditer(r'<table[^>]*sortable[^>]*>(.*?)</table>', html, re.DOTALL))
print(f"Tables: {len(tables)}")

cn_players = {}
for st in tables:
    tp = st.start()
    # Find closest h3 before this table
    before = html[:tp]
    h3s = list(re.finditer(r'<h3[>\s].*?</h3>', before, re.DOTALL))
    if not h3s: continue
    
    h_text = re.sub(r'<[^>]+>', '', h3s[-1].group(0)).strip()
    h_text = re.sub(r'\[.*?\]', '', h_text).strip()
    if len(h_text) < 1 or len(h_text) > 30: continue
    
    # Extract players from rows using text approach
    rows = re.findall(r'<tr>(.*?)</tr>', st.group(1), re.DOTALL)
    players = []
    for row in rows[1:]:  # skip header
        text = re.sub(r'<[^>]+>', ' ', row)
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        # Pattern: number position ChineseName ...
        m = re.match(r'(\d+)\s+(\S+)\s+(\S+)', text)
        if m:
            name = m.group(3)
            # Clean: remove parenthetical notes but keep the name
            name = re.sub(r'\[.*?\]', '', name)
            if 2 <= len(name) <= 30:
                players.append(name)
    
    if players:
        cn_players[h_text] = players

# Save
with open('E:/Workspace/Kun/WCUP2026/data/cn_players.json', 'w', encoding='utf-8') as f:
    json.dump(cn_players, f, ensure_ascii=False, indent=2)

# Print stats (write to file to avoid encoding issues)
with open('E:/Workspace/Kun/WCUP2026/data/cn_players_stats.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total: {len(cn_players)} teams, {sum(len(p) for p in cn_players.values())} players\n\n")
    for t in sorted(cn_players.keys()):
        pl = cn_players[t]
        f.write(f"{t}: {len(pl)} players\n")
        f.write(f"  {', '.join(pl[:5])}\n")

print(f"Done! {len(cn_players)} teams, {sum(len(p) for p in cn_players.values())} players")
print("Stats saved to data/cn_players_stats.txt")
