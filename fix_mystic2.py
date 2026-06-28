with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: onchange for mystic
html = html.replace(
    'onchange="renderAll();setTimeout(loadMysticDetail,200);"',
    'onchange="currentMysticTeam=this.value;renderAll();"'
)

# Fix 2: Add selected attribute to mystic options
old_opt = "for(var i=0; i<Math.min(allTeams.length, 30); i++) h += '<option value=\"' + allTeams[i] + '\">' + cn(allTeams[i]) + '</option>';"
new_opt = """for(var i=0; i<Math.min(allTeams.length, 30); i++){
    var mt = allTeams[i];
    h += '<option value="' + mt + '"' + (mt === currentMysticTeam ? ' selected' : '') + '>' + cn(mt) + '</option>';
  }"""
html = html.replace(old_opt, new_opt)

# Fix 3: loadMysticDetail to use global instead of DOM read
html = html.replace(
    "var sel = document.getElementById('mystic-team');",
    ""
)
html = html.replace(
    "var team = (sel && sel.value) ? sel.value : allTeams[0];",
    "var team = currentMysticTeam || allTeams[0];"
)

# Fix 4: Add currentMysticTeam declaration and init
html = html.replace(
    "// ── 3. 玄学分析 ──\nfunction renderMystic(){",
    "// ── 3. 玄学分析 ──\nvar currentMysticTeam = null;\nfunction renderMystic(){\n  if(!currentMysticTeam) currentMysticTeam = allTeams[0];"
)

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Mystic dropdown fixed')
