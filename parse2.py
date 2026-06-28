import re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('E:/Workspace/Kun/WCUP2026/wiki_main.html', 'r', encoding='utf-8') as f:
    html = f.read()

li_pattern = re.compile(r'<li>(.*?)</li>', re.DOTALL)
goalscorers = {}
for m in li_pattern.finditer(html):
    content = m.group(1)
    n = content.count('class="fb-goal"')
    if n > 0:
        nm = re.search(r'<a[^>]*>([^<]+)</a>', content)
        if nm:
            name = nm.group(1).strip()
            if len(name) >= 2:
                goalscorers[name] = goalscorers.get(name, 0) + n

sg = sorted(goalscorers.items(), key=lambda x: x[1], reverse=True)
with open('E:/Workspace/Kun/WCUP2026/data/wc_goalscorers.json', 'w', encoding='utf-8') as f:
    json.dump(dict(sg), f, indent=2, ensure_ascii=False)
print(f'OK: {len(goalscorers)} scorers, {sum(goalscorers.values())} goals')
