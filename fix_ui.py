with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Add WC goals loading in init after allTeams.sort()
h = h.replace('allTeams.sort();', 
    'allTeams.sort();\n    try{ var gr = await fetch(\'/api/wc_goals\'); if(gr.ok) window.wcGoals = await gr.json(); }catch(e){}')

# Add column header
h = h.replace('<th>进球</th>', '<th>生涯进球</th><th>本届进球</th>')

# Add WC goals to each player row
h = h.replace(
    "(p.goals || p.national_goals || '-') + '</td><td style=\"",
    "(p.goals || p.national_goals || '-') + '</td><td>' + (window.wcGoals && p.name && window.wcGoals[p.name] ? window.wcGoals[p.name] : '-') + '</td><td style=\""
)

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Frontend updated')
