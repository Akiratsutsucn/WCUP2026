with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Fix squad dropdown - find the exact line
old_squad = "for(var i=0; i<allTeams.length; i++) h += '<option value=\"' + allTeams[i] + '\">' + cn(allTeams[i]) + '</option>';"
new_squad = "var sqTeams = (window.r32Teams && window.r32Teams.length > 0) ? window.r32Teams : allTeams; for(var i=0; i<sqTeams.length; i++) h += '<option value=\"' + sqTeams[i] + '\">' + cn(sqTeams[i]) + '</option>';"

h = h.replace(old_squad, new_squad)
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Fixed')
