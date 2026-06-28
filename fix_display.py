with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix 1: Mystic display - replace JSON.stringify with formatted Chinese
old_mystic = "document.getElementById('mystic-detail').innerHTML = '<pre style=\"white-space:pre-wrap;font-size:.75em;\">' + JSON.stringify(d, null, 2) + '</pre>';"

new_mystic = """  var h = '';
  if(d.error){ h += '<p style=\"color:#e88;\">错误：' + d.error + '</p>'; }
  else {
    var ts = d.three_stages || {};
    h += '<div class=\"card\" style=\"padding:10px;margin:6px 0;\"><b style=\"color:#f0d878;\">【第一境 · 看山是山】</b><br>' + (ts.stage1||'暂无') + '</div>';
    h += '<div class=\"card\" style=\"padding:10px;margin:6px 0;\"><b style=\"color:#f0d878;\">【第二境 · 看山不是山】</b><br>' + (ts.stage2||'暂无') + '</div>';
    h += '<div class=\"card\" style=\"padding:10px;margin:6px 0;\"><b style=\"color:#f0d878;\">【第三境 · 看山还是山】</b><br>' + (ts.stage3||'暂无') + '</div>';
    h += '<div class=\"card\" style=\"padding:10px;margin:6px 0;\"><b style=\"color:#c9a84c;\">【道德经】</b><br>' + (d.tao_te_ching||'暂无') + '</div>';
    h += '<div class=\"card\" style=\"padding:10px;margin:6px 0;\"><b style=\"color:#c9a84c;\">【易经卦象】</b><br>' + (d.i_ching||'暂无') + '</div>';
    if(d.elo) h += '<div style=\"font-size:.75em;color:#7aa4c8;margin-top:4px;\">Elo：' + d.elo + '</div>';
  }
  document.getElementById('mystic-detail').innerHTML = h;"""

html = html.replace(old_mystic, new_mystic)

# Fix 2: H2H display - add predicted score
old_h2h_score = "'<div class=\"text-center mt-8\" style=\"font-size:.75em;color:#7aa4c8;\">预期进球：' + cn(d.team_a) + ' ' + (d.expected_goals_a||'暂无') + ' — ' + (d.expected_goals_b||'暂无') + ' ' + cn(d.team_b) + '</div>' +"

new_h2h_score = """'<div class=\"text-center mt-8\" style=\"font-size:.75em;color:#7aa4c8;\">预期进球：' + cn(d.team_a) + ' ' + (d.expected_goals_a||'?').toFixed(1) + ' — ' + (d.expected_goals_b||'?').toFixed(1) + ' ' + cn(d.team_b) + '<br>预测比分：' + cn(d.team_a) + ' ' + Math.round(d.expected_goals_a||0) + ' - ' + Math.round(d.expected_goals_b||0) + ' ' + cn(d.team_b) + '</div>' +"""

html = html.replace(old_h2h_score, new_h2h_score)

# Fix 3: Remove flag emoji spans from bracket and H2H display  
html = html.replace("'<span class=\"flag\" style=\"font-size:1em;\">' + getFlag(home) + '</span>'", "''")
html = html.replace("'<span class=\"flag\" style=\"font-size:1em;\">' + getFlag(away) + '</span>'", "''")
html = html.replace("'<div class=\"flag\">' + getFlag(d.team_a) + '</div>'", "''")
html = html.replace("'<div class=\"flag\">' + getFlag(d.team_b) + '</div>'", "''")

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Mystic display + H2H score prediction fixed')
