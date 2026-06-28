import re, json

with open('E:/Workspace/Kun/WCUP2026/wiki_main.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the Goalscorers section
idx = html.find('id="Goalscorers"')
if idx < 0:
    for i in range(len(html)):
        if 'Goalscorers' in html[i:i+20] and 'mw-headline' in html[i-50:i]:
            idx = i
            break

# Get section until next h2
end = html.find('<h2>', idx) if idx > 0 else -1
section = html[idx:end] if idx > 0 and end > idx else html

# Find ALL goal entries: each is <li><a href="...">PlayerName</a> <span class="fb-goal">
goalscorers = {}
li_matches = re.finditer(r'<li>(.*?)</li>', section, re.DOTALL)

for li in li_matches:
    content = li.group(1)
    # Count goal spans
    goal_count = len(re.findall(r'class="fb-goal"', content))
    if goal_count == 0:
        continue
    
    # Extract player name from the link
    name_match = re.search(r'<a[^>]*>([^<]+)</a>', content)
    if name_match:
        name = name_match.group(1).strip()
        # Skip non-player entries
        if len(name) < 2 or name in ('Goal', 'Penalty'):
            continue
        goalscorers[name] = goalscorers.get(name, 0) + goal_count

sorted_g = sorted(goalscorers.items(), key=lambda x: x[1], reverse=True)
print(f"Found {len(goalscorers)} goalscorers, {sum(goalscorers.values())} total goals")
for name, goals in sorted_g[:25]:
    print(f"  {name}: {goals}")

with open('E:/Workspace/Kun/WCUP2026/data/wc_goalscorers.json', 'w', encoding='utf-8') as f:
    json.dump(dict(sorted_g), f, indent=2, ensure_ascii=False)
print(f"\nSaved {len(goalscorers)} scorers to wc_goalscorers.json")
