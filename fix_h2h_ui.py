with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Fix H2H predicted score line to use the new API field
old = "'<div class=\"text-center mt-8\" style=\"font-size:.75em;color:#7aa4c8;\">预期进球：' + cn(d.team_a) + ' ' + (d.expected_goals_a||'?').toFixed(1) + ' — ' + (d.expected_goals_b||'?').toFixed(1) + ' ' + cn(d.team_b) + '<br>预测比分：' + cn(d.team_a) + ' ' + Math.round(d.expected_goals_a||0) + ' - ' + Math.round(d.expected_goals_b||0) + ' ' + cn(d.team_b) + '</div>'"

new = "'<div class=\"text-center mt-8\" style=\"font-size:.75em;color:#7aa4c8;\">预期进球：' + cn(d.team_a) + ' ' + (d.expected_goals_a||'?').toFixed(1) + ' — ' + (d.expected_goals_b||'?').toFixed(1) + ' ' + cn(d.team_b) + '<br>预测比分（90分钟常规时间）：' + cn(d.team_a) + ' ' + (d.predicted_score||'?-?') + ' ' + cn(d.team_b) + '</div>'"

if old in h:
    h = h.replace(old, new)
    print('Frontend H2H updated')
else:
    print('Pattern not found - checking partial...')
    # Try partial match
    if '预测比分' in h:
        print('预测比分 found in HTML')
    else:
        print('预测比分 NOT in HTML')

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
