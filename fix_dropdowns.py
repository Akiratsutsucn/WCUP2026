with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Move currentFactorTeam outside renderFactor function
html = html.replace(
    '// \u2500\u2500 2. \u56e0\u5b50\u5206\u6790 \u2500\u2500\nvar currentFactorTeam = null;\nfunction renderFactor(){',
    'var currentFactorTeam = null;\n// \u2500\u2500 2. \u56e0\u5b50\u5206\u6790 \u2500\u2500\nfunction renderFactor(){'
)

# Fix 2: Fix factor onchange
html = html.replace(
    '<select id="factor-team" onchange="renderAll()">',
    '<select id="factor-team" onchange="currentFactorTeam=this.value;renderAll();">'
)

# Fix 3: Fix mystic onchange
html = html.replace(
    '<select id="mystic-team" onchange="renderAll()">',
    '<select id="mystic-team" onchange="renderAll();">'
)

# Fix 4: Remove duplicate initialization (the line inside function that sets currentFactorTeam)
html = html.replace(
    "if(!currentFactorTeam && predictData && predictData.rankings && predictData.rankings.length) currentFactorTeam = predictData.rankings[0].team;\n  if(!predictData || !predictData.rankings || !predictData.rankings.length)",
    "if(!currentFactorTeam && predictData && predictData.rankings && predictData.rankings.length) currentFactorTeam = predictData.rankings[0].team;\n  if(!predictData || !predictData.rankings || !predictData.rankings.length)"
)

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Fixed')
