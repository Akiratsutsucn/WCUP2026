
// 轮次中文名称映射
var ROUND_NAMES_CN = {
  R32: '32强淘汰赛', R16: '16强淘汰赛', QF: '四分之一决赛',
  SF: '半决赛', '3rd': '季军争夺赛', F: ' 冠军决赛'
};

var matchData = null, standingsData = null, predictData = null, editingMatchId = null, allTeams = [], teamsData = null;

async function init(){
  try{
    var r = await fetch('/api/all');
    var d = await r.json();
    matchData = d.matches;
    standingsData = d.standings;
    teamsData = d.teams;
    if(standingsData) for(var g in standingsData) for(var i=0; i<standingsData[g].length; i++)
      if(allTeams.indexOf(standingsData[g][i].team) < 0) allTeams.push(standingsData[g][i].team);
    allTeams.sort();
    try{
      var p = await fetch('/api/predict/all');
      if(p.ok) predictData = await p.json();
    }catch(e){}
    renderAll();
  }catch(e){
    document.getElementById('app').innerHTML = '<div class="error">加载失败：' + e.message + '</div>';
  }
}

document.getElementById('nav').addEventListener('click', function(e){
  if(!e.target.classList.contains('nav-btn')) return;
  document.querySelectorAll('.nav-btn').forEach(function(b){ b.classList.remove('active'); });
  e.target.classList.add('active');
  renderAll();
});

function activeTab(){
  var btn = document.querySelector('.nav-btn.active');
  return btn ? btn.dataset.tab : 'predict';
}

function renderAll(){
  var tab = activeTab(), html = '';
  switch(tab){
    case 'predict': html = renderPredict(); break;
    case 'factor': html = renderFactor(); break;
    case 'mystic': html = renderMystic(); break;
    case 'h2h': html = renderH2H(); break;
    case 'squad': html = renderSquad(); break;
    case 'susp': html = renderSuspensions(); break;
    case 'bracket': html = renderBracketPage(); break;
  }
  document.getElementById('app').innerHTML = html;
}

// ── 1. 冠军预测 ──
function renderPredict(){
  if(!currentFactorTeam && predictData && predictData.rankings && predictData.rankings.length) currentFactorTeam = predictData.rankings[0].team;
  if(!predictData || !predictData.rankings || !predictData.rankings.length)
    return '<div class="card"><h3> 冠军预测排行</h3><div class="loading">预测引擎正在启动，请稍候...</div></div>';
  var r = predictData.rankings;
  var maxProb = 0;
  for(var i=0; i<r.length; i++){ var prob = r[i].adjusted_prob || 0; if(prob > maxProb) maxProb = prob; }
  if(maxProb <= 0) maxProb = 20;
  var h = '<div class="card"><h3> 冠军预测排行 — 蒙特卡洛模拟</h3>';
  h += '<div class="btn-bar"><button class="btn-sm" onclick="location.reload()">刷新 刷新预测</button></div>';
  for(var i=0; i<Math.min(r.length, 20); i++){
    var t = r[i], prob = t.adjusted_prob || 0;
    var barW = prob / maxProb * 100;
    h += '<div class="ranking-bar"><span class="rk">' + (i+1) + '</span><span class="flag">' + getFlag(t.team) + '</span>';
    h += '<span class="name">' + cn(t.team) + '</span>';
    h += '<div class="bar-wrap"><div class="bar-fill" style="width:' + barW + '%"></div></div>';
    h += '<span class="prob">' + prob.toFixed(1) + '%</span></div>';
  }
  h += '<div class="mt-8" style="font-size:.75em;color:#7aa4c8;">基于：实力评分 + 球员数据 + 球队因子 + 玄学修正</div>';
  return h + '</div>';
}

var currentFactorTeam = null;
// ── 2. 因子分析 ──
function renderFactor(){
  if(!predictData || !predictData.rankings || !predictData.rankings.length)
    return '<div class="card"><h3> 球队因子分析</h3><div class="loading">数据加载中...</div></div>';
  var h = '<div class="card"><h3> 球队评分因子构成</h3>';
  h += '<div class="btn-bar"><select id="factor-team" onchange="currentFactorTeam=this.value;renderAll();">';
  for(var i=0; i<Math.min(predictData.rankings.length, 20); i++)
    var tn = predictData.rankings[i].team; h += '<option value="' + tn + '"' + (tn === currentFactorTeam ? ' selected' : '') + '>' + cn(tn) + '</option>';
  h += '</select></div>';
  var t = predictData.rankings.find(function(x){ return x.team === currentFactorTeam; });
  var t = predictData.rankings.find(function(x){ return x.team === sel; });
  if(t){
    h += '<div class="factor-grid">';
    h += '<div class="factor-tag"><span>实力评分</span><span class="val">' + (t.elo || '暂无') + '</span></div>';
    h += '<div class="factor-tag"><span>球员数量</span><span class="val">' + (t.player_count || '暂无') + '</span></div>';
    h += '<div class="factor-tag"><span>平均年龄</span><span class="val">' + (t.avg_age || '暂无') + '</span></div>';
    h += '<div class="factor-tag"><span>综合得分</span><span class="val">' + (t.total_score || t.score || '暂无') + '</span></div>';
    h += '<div class="factor-tag"><span>原始概率</span><span class="val">' + ((t.raw_prob||0).toFixed(2)) + '%</span></div>';
    var adj = t.mystic_adjustment || 0;
    h += '<div class="factor-tag"><span>玄学修正</span><span class="val">' + (adj>0?'+':'') + adj.toFixed(2) + '%</span></div>';
    h += '<div class="factor-tag"><span>调整后概率</span><span class="val">' + ((t.adjusted_prob||0).toFixed(2)) + '%</span></div>';
    h += '</div>';
  }
  if(predictData.ucl_signals){
    h += '<div class="card mt-8"><h3> 欧冠决赛心态信号</h3>';
    var sigs = predictData.ucl_signals;
    var count = 0;
    for(var k in sigs){
      if(sigs[k] && typeof sigs[k] === 'object' && count < 15){
        h += '<div class="factor-tag"><span>' + k + '</span><span class="val">' + JSON.stringify(sigs[k]).slice(0,60) + '</span></div>';
        count++;
      }
    }
    if(count === 0) h += '<div style="font-size:.75em;color:#556;">暂无欧冠决赛相关心态信号数据</div>';
    h += '</div>';
  }
  return h + '</div>';
}

// ── 3. 玄学分析 ──
function renderMystic(){
  if(!predictData)
    return '<div class="card"><h3> 玄学分析</h3><div class="loading">玄学数据加载中...</div></div>';
  var h = '<div class="card"><h3> 玄学因子 — 悖论框架 · 道德经 · 易经</h3>';
  h += '<p style="font-size:.78em;color:#7aa4c8;margin-bottom:10px;">三重境界：看山是山 → 看山不是山 → 看山还是山</p>';
  h += '<div class="btn-bar"><select id="mystic-team" onchange="renderAll();setTimeout(loadMysticDetail,200);">';
  for(var i=0; i<Math.min(allTeams.length, 30); i++) h += '<option value="' + allTeams[i] + '">' + cn(allTeams[i]) + '</option>';
  h += '</select><button class="btn-sm" onclick="loadMysticDetail()">查看详情</button></div>';
  h += '<div id="mystic-detail" class="mt-8" style="font-size:.8em;color:#a0b8d0;"></div>';
  h += '</div>';
  setTimeout(loadMysticDetail, 300);
  return h;
}
async function loadMysticDetail(){
  var sel = document.getElementById('mystic-team');
  var team = (sel && sel.value) ? sel.value : allTeams[0];
  var r = await fetch('/api/predict/mystic?team=' + encodeURIComponent(team));
  var d = await r.json();
    var h = '';
  if(d.error){ h += '<p style="color:#e88;">错误：' + d.error + '</p>'; }
  else {
    var ts = d.three_stages || {};
    h += '<div class="card" style="padding:10px;margin:6px 0;"><b style="color:#f0d878;">【第一境 · 看山是山】</b><br>' + (ts.stage1||'暂无') + '</div>';
    h += '<div class="card" style="padding:10px;margin:6px 0;"><b style="color:#f0d878;">【第二境 · 看山不是山】</b><br>' + (ts.stage2||'暂无') + '</div>';
    h += '<div class="card" style="padding:10px;margin:6px 0;"><b style="color:#f0d878;">【第三境 · 看山还是山】</b><br>' + (ts.stage3||'暂无') + '</div>';
    h += '<div class="card" style="padding:10px;margin:6px 0;"><b style="color:#c9a84c;">【道德经】</b><br>' + (d.tao_te_ching||'暂无') + '</div>';
    h += '<div class="card" style="padding:10px;margin:6px 0;"><b style="color:#c9a84c;">【易经卦象】</b><br>' + (d.i_ching||'暂无') + '</div>';
    if(d.elo) h += '<div style="font-size:.75em;color:#7aa4c8;margin-top:4px;">实力：' + d.elo + '</div>';
  }
  document.getElementById('mystic-detail').innerHTML = h;
}

// ── 4. 对战预测 ──
function renderH2H(){
  if(!matchData || !matchData.matches) return '<div class="card"><h3> 对战预测</h3><div class="loading">数据加载中...</div></div>';
  var r32matches = matchData.matches.filter(function(m){ return m.round === 'R32'; }).sort(function(a,b){ return a.id.localeCompare(b.id); });
  var h = '<div class="card"><h3> 32强对战预测</h3>';
  h += '<p style="font-size:.78em;color:#7aa4c8;margin-bottom:10px;">点击任意对阵查看详细预测分析</p>';
  h += '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;">';
  for(var i=0; i<r32matches.length; i++){
    var m = r32matches[i];
    var home = m.home || '待定', away = m.away || '待定';
    h += '<div class="ranking-bar" onclick="loadH2H(\'' + home + '\',\'' + away + '\')" style="cursor:pointer;padding:6px 8px;font-size:.78em;" title="点击查看预测">';
    h += '<span class="flag" style="font-size:1em;">' + getFlag(home) + '</span><span style="font-size:.8em;">' + cn(home) + '</span>';
    h += '<span style="color:#c9a84c;font-size:.7em;margin:0 2px;">vs</span>';
    h += '<span class="flag" style="font-size:1em;">' + getFlag(away) + '</span><span style="font-size:.8em;">' + cn(away) + '</span>';
    h += '</div>';
  }
  h += '</div><div id="h2h-result" class="mt-8"></div>';
  return h + '</div>';
}
async function loadH2H(ta, tb){
  if(!ta || !tb){ document.getElementById('h2h-result').innerHTML=''; return; }
  document.getElementById('h2h-result').innerHTML = '<div class="loading" style="padding:20px;">正在分析 ' + cn(ta) + ' vs ' + cn(tb) + '...</div>';
  try{
    var r = await fetch('/api/predict/h2h?team1=' + encodeURIComponent(ta) + '&team2=' + encodeURIComponent(tb));
    var d = await r.json();
    if(d.error){ document.getElementById('h2h-result').innerHTML = '<div class="error">请求失败：' + d.error + '</div>'; return; }
    document.getElementById('h2h-result').innerHTML =
      '<div class="card" style="margin-top:10px;">' +
      '<div class="h2h-compare">' +
        '<div class="h2h-team"><div class="flag">' + getFlag(d.team_a) + '</div><div class="name">' + cn(d.team_a) + '</div><div class="elo">实力：' + (d.elo_a||'暂无') + '</div></div>' +
        '<div class="h2h-vs">对阵</div>' +
        '<div class="h2h-team"><div class="flag">' + getFlag(d.team_b) + '</div><div class="name">' + cn(d.team_b) + '</div><div class="elo">实力：' + (d.elo_b||'暂无') + '</div></div>' +
      '</div>' +
      '<div class="h2h-probs">' +
        '<div><div class="p">' + ((d.win_prob_a||0).toFixed(1)) + '%</div><div class="l">' + cn(d.team_a) + ' 胜</div></div>' +
        '<div><div class="p">' + ((d.draw_prob||0).toFixed(1)) + '%</div><div class="l">平局</div></div>' +
        '<div><div class="p">' + ((d.win_prob_b||0).toFixed(1)) + '%</div><div class="l">' + cn(d.team_b) + ' 胜</div></div>' +
      '</div>' +
      '<div class="text-center mt-8" style="font-size:.75em;color:#7aa4c8;">预期进球：' + cn(d.team_a) + ' ' + (d.expected_goals_a||'?').toFixed(1) + ' — ' + (d.expected_goals_b||'?').toFixed(1) + ' ' + cn(d.team_b) + '<br>预测比分：' + cn(d.team_a) + ' ' + Math.round(d.expected_goals_a||0) + ' - ' + Math.round(d.expected_goals_b||0) + ' ' + cn(d.team_b) + '</div>' +
      '</div>';
  }catch(e){
    document.getElementById('h2h-result').innerHTML = '<div class="error">预测失败：' + e.message + '</div>';
  }
}

// ── 5. 球员阵容 ──
function renderSquad(){
  var h = '<div class="card"><h3> 球员阵容</h3>';
  h += '<div class="btn-bar"><select id="squad-team" onchange="loadSquad()">';
  for(var i=0; i<allTeams.length; i++) h += '<option value="' + allTeams[i] + '">' + cn(allTeams[i]) + '</option>';
  h += '</select></div><div id="squad-result" class="squad-list"></div>';
  h += '</div>';
  setTimeout(loadSquad, 100);
  return h;
}
async function loadSquad(){
  var sel = document.getElementById('squad-team');
  var team = (sel && sel.value) ? sel.value : allTeams[0];
  try{
    var r = await fetch('/api/predict/squad?team=' + encodeURIComponent(team));
    var d = await r.json();
    if(d.error){ document.getElementById('squad-result').innerHTML = '<div class="error">请求失败：' + d.error + '</div>'; return; }
    var players = d.players || [];
    if(!players.length){ document.getElementById('squad-result').innerHTML = '<div class="loading">该队暂无阵容数据</div>'; return; }
    var tbl = '<table><thead><tr><th>#</th><th>姓名</th><th>位置</th><th>年龄</th><th>国家队出场</th><th>国家队进球</th><th>俱乐部</th></tr></thead><tbody>';
    players.slice(0, 26).forEach(function(p, i){
      tbl += '<tr><td>' + (i+1) + '</td><td>' + (p.name_cn || p.name || p.player_name || '未知') + '</td><td>' + (p.position || p.pos || '-') + '</td><td>' + (p.age || '-') + '</td><td>' + (p.caps || p.national_caps || '-') + '</td><td>' + (p.goals || p.national_goals || '-') + '</td><td>' + (p.club || '-') + '</td></tr>';
    });
    tbl += '</tbody></table>';
    document.getElementById('squad-result').innerHTML = tbl;
  }catch(e){
    document.getElementById('squad-result').innerHTML = '<div class="error">加载失败：' + e.message + '</div>';
  }
}

// ── 6. 伤病停赛 ──
function renderSuspensions(){
  if(!predictData || !predictData.suspensions)
    return '<div class="card"><h3> 伤病与停赛追踪</h3><div class="loading">数据加载中...</div></div>';
  var s = predictData.suspensions;
  var h = '<div class="card"><h3> 伤病与停赛追踪</h3>';
  if(s.injuries){
    h += '<h4 style="color:#e88;margin:10px 0 6px;"> 伤病情况</h4>';
    var hasInj = false;
    for(var team in s.injuries){
      if(!s.injuries[team].length) continue;
      hasInj = true;
      h += '<div class="card" style="padding:10px;"><b>' + getFlag(team) + ' ' + cn(team) + '</b><br>';
      for(var i=0; i<s.injuries[team].length; i++){
        var inj = s.injuries[team][i];
        var badge = inj.impact === 'high' ? 'badge-red' : (inj.impact === 'medium' ? 'badge-yellow' : 'badge-green');
        h += '<span class="badge ' + badge + '">' + inj.status + '</span> ' + inj.player + ' — ' + inj.detail + '<br>';
      }
      h += '</div>';
    }
    if(!hasInj) h += '<div style="font-size:.75em;color:#556;">暂无伤病报告</div>';
  }
  if(s.suspensions){
    h += '<h4 style="color:#fc8;margin:10px 0 6px;"> 停赛情况</h4>';
    var hasSus = false;
    for(var team in s.suspensions){
      if(!s.suspensions[team].length) continue;
      hasSus = true;
      h += '<div class="card" style="padding:10px;"><b>' + getFlag(team) + ' ' + cn(team) + '</b><br>';
      for(var i=0; i<s.suspensions[team].length; i++){
        var sus = s.suspensions[team][i];
        h += '<span class="badge badge-red">停赛</span> ' + sus.player + ' — ' + sus.reason + '（' + sus.match + '）<br>';
      }
      h += '</div>';
    }
    if(!hasSus) h += '<div style="font-size:.75em;color:#556;">暂无停赛球员</div>';
  }
  if(s.card_counts){
    h += '<h4 style="color:#7aa4c8;margin:10px 0 6px;"> 红黄牌统计</h4>';
    h += '<div class="factor-grid">';
    for(var team in s.card_counts){
      var c = s.card_counts[team];
      h += '<div class="factor-tag"><span>' + getFlag(team) + ' ' + team + '</span><span> ' + (c.yellow||0) + ' 张 &nbsp;  ' + (c.red||0) + ' 张</span></div>';
    }
    h += '</div>';
  }
  return h + '</div>';
}

// ── 7. 淘汰赛对阵 ──
function renderBracketPage(){
  var h = '<div class="card"><h3> 淘汰赛对阵图 — 32强 → 决赛</h3>';
  h += '<div class="btn-bar"><button class="btn-sm" onclick="fillR32()">刷新 自动填充32强</button><button class="btn-sm" onclick="resetBracket()" style="background:#5a3030;color:#e88;">! 重置全部比赛</button></div>';
  h += '<div id="bracket-svg-container" style="overflow-x:auto;"></div>';
  h += '</div>';
  setTimeout(function(){ drawBracketSVG(); }, 150);
  return h;
}

function drawBracketSVG(){
  if(!matchData || !matchData.matches) return;
  var ms = matchData.matches;
  var matchById = {}; ms.forEach(function(m){ matchById[m.id] = m; });
  
  var rounds = ['R32','R16','QF','SF','F','3rd'];
  var labels = ['32强','16强','1/4决赛','半决赛',' 决赛','季军赛'];
  var BOX_W = 155, BOX_H = 47, GAP_Y = 56;
  var X = [10, 215, 420, 625, 830, 1035];
  
  // Build position map
  var pos = {};
  function getRound(round, sort){
    return ms.filter(function(m){ return m.round===round; }).sort(function(a,b){ return a.id.localeCompare(b.id); });
  }
  
  var r32 = getRound('R32');
  for(var i=0; i<r32.length; i++) pos[r32[i].id] = {x:X[0], y:25 + i*GAP_Y};
  
  var r16 = getRound('R16');
  for(var i=0; i<r16.length; i++){
    var y1 = pos[r32[i*2].id].y, y2 = pos[r32[i*2+1].id].y;
    pos[r16[i].id] = {x:X[1], y:(y1+y2+BOX_H)/2 - BOX_H/2};
  }
  
  var qf = getRound('QF');
  for(var i=0; i<qf.length; i++){
    var y1 = pos[r16[i*2].id].y, y2 = pos[r16[i*2+1].id].y;
    pos[qf[i].id] = {x:X[2], y:(y1+y2+BOX_H)/2 - BOX_H/2};
  }
  
  var sf = getRound('SF');
  for(var i=0; i<sf.length; i++){
    var y1 = pos[qf[i*2].id].y, y2 = pos[qf[i*2+1].id].y;
    pos[sf[i].id] = {x:X[3], y:(y1+y2+BOX_H)/2 - BOX_H/2};
  }
  
  var fm = getRound('F')[0];
  var tpm = getRound('3rd')[0];
  if(fm && sf.length>=2){
    var y1 = pos[sf[0].id].y, y2 = pos[sf[1].id].y;
    pos[fm.id] = {x:X[4], y:(y1+y2+BOX_H)/2 - BOX_H/2};
  }
  if(tpm) pos[tpm.id] = {x:X[5], y: pos[fm.id] ? pos[fm.id].y : 400};
  
  var maxY = 25 + 15*GAP_Y + BOX_H + 20;
  var svgW = X[5] + BOX_W + 20;
  
  var svg = '<svg width="' + svgW + '" height="' + maxY + '" style="background:#0a0f1a;font-family:system-ui,sans-serif;">';
  
  // Connector lines
  svg += '<g stroke="#c9a84c" stroke-width="2" fill="none" opacity="0.6">';
  for(var mid in pos){
    var m = matchById[mid]; if(!m || !m.next) continue;
    var p1 = pos[mid], p2 = pos[m.next]; if(!p1 || !p2) continue;
    var x1 = p1.x + BOX_W, y1 = p1.y + BOX_H/2;
    var x2 = p2.x, y2 = p2.y + BOX_H/2;
    var mx = (x1 + x2) / 2;
    svg += '<path d="M' + x1 + ',' + y1 + ' L' + mx + ',' + y1 + ' L' + mx + ',' + y2 + ' L' + x2 + ',' + y2 + '"/>';
  }
  // 3rd place dashed lines from SF losers
  if(tpm && sf.length>=2){
    for(var i=0; i<2; i++){
      var sx = pos[sf[i].id].x + BOX_W, sy = pos[sf[i].id].y + BOX_H*0.75;
      var tx = pos[tpm.id].x, ty = pos[tpm.id].y + BOX_H/2;
      var mx2 = sx + 25;
      svg += '<path d="M' + sx + ',' + sy + ' L' + mx2 + ',' + sy + ' L' + mx2 + ',' + ty + ' L' + tx + ',' + ty + '" stroke="#a08040" stroke-dasharray="5,3"/>';
    }
  }
  svg += '</g>';
  
  // Round titles
  svg += '<g fill="#f0d878" font-size="12" font-weight="bold" text-anchor="middle">';
  for(var i=0; i<rounds.length; i++)
    svg += '<text x="' + (X[i] + BOX_W/2) + '" y="14">' + labels[i] + '</text>';
  svg += '</g>';
  
  // Match boxes
  for(var mid in pos){
    var p = pos[mid], m = matchById[mid]; if(!m) continue;
    var home = m.home ? cn(m.home) : '待定', away = m.away ? cn(m.away) : '待定';
    var hs = m.home_score!=null ? m.home_score : '-', as = m.away_score!=null ? m.away_score : '-';
    var hw = m.winner==='home', aw = m.winner==='away';
    var fill = m.winner ? '#0a1a10' : '#0f1a2e', border = m.winner ? '#2a5a30' : '#1a3050';
    
    svg += '<g onclick="openModal(\'' + mid + '\')" style="cursor:pointer">';
    svg += '<rect x="' + p.x + '" y="' + p.y + '" width="' + BOX_W + '" height="' + BOX_H + '" rx="6" fill="' + fill + '" stroke="' + border + '" stroke-width="1.5"/>';
    svg += '<text x="' + (p.x+6) + '" y="' + (p.y+18) + '" fill="' + (hw?'#f0d878':'#c0c8d8') + '" font-size="11" font-weight="' + (hw?'bold':'normal') + '">' + home.substring(0,14) + '</text>';
    svg += '<text x="' + (p.x+BOX_W-6) + '" y="' + (p.y+18) + '" fill="#f0d878" font-size="11" font-weight="bold" text-anchor="end">' + hs + '</text>';
    svg += '<line x1="' + (p.x+4) + '" y1="' + (p.y+BOX_H/2) + '" x2="' + (p.x+BOX_W-4) + '" y2="' + (p.y+BOX_H/2) + '" stroke="#1a3050" stroke-width="1"/>';
    svg += '<text x="' + (p.x+6) + '" y="' + (p.y+40) + '" fill="' + (aw?'#f0d878':'#c0c8d8') + '" font-size="11" font-weight="' + (aw?'bold':'normal') + '">' + away.substring(0,14) + '</text>';
    svg += '<text x="' + (p.x+BOX_W-6) + '" y="' + (p.y+40) + '" fill="#f0d878" font-size="11" font-weight="bold" text-anchor="end">' + as + '</text>';
    svg += '</g>';
  }
  
  svg += '</svg>';
  document.getElementById('bracket-svg-container').innerHTML = svg;
}

// ── 编辑弹窗 ──
function openModal(id){
  editingMatchId = id;
  var m = matchData.matches.find(function(x){ return x.id === id; });
  if(!m) return;
  var rn = ROUND_NAMES_CN[m.round] || (matchData.rounds[m.round] ? matchData.rounds[m.round].name : m.round);
  document.getElementById('modal-info').innerHTML = '<b>' + rn + '</b> — ' + (m.date||'') + '<br> ' + (m.venue||'');
  var opts = '<option value="">-- 请选择 --</option>';
  for(var i=0; i<allTeams.length; i++) opts += '<option value="\' + allTeams[i] + \'">\' + cn(allTeams[i]) + \'</option>';
  document.getElementById('m-home').innerHTML = opts;
  document.getElementById('m-away').innerHTML = opts;
  document.getElementById('m-home').value = m.home || '';
  document.getElementById('m-away').value = m.away || '';
  document.getElementById('m-hs').value = m.home_score !== null && m.home_score !== undefined ? m.home_score : '';
  document.getElementById('m-as').value = m.away_score !== null && m.away_score !== undefined ? m.away_score : '';
  document.getElementById('m-hp').value = m.home_pen !== null && m.home_pen !== undefined ? m.home_pen : '';
  document.getElementById('m-ap').value = m.away_pen !== null && m.away_pen !== undefined ? m.away_pen : '';
  document.getElementById('modal').classList.add('show');
}
function closeModal(){
  document.getElementById('modal').classList.remove('show');
  editingMatchId = null;
}
async function saveMatch(){
  var home = document.getElementById('m-home').value, away = document.getElementById('m-away').value;
  var hs = document.getElementById('m-hs').value === '' ? null : parseInt(document.getElementById('m-hs').value);
  var as = document.getElementById('m-as').value === '' ? null : parseInt(document.getElementById('m-as').value);
  var hp = document.getElementById('m-hp').value === '' ? null : parseInt(document.getElementById('m-hp').value);
  var ap = document.getElementById('m-ap').value === '' ? null : parseInt(document.getElementById('m-ap').value);
  if(hs === null || as === null || isNaN(hs) || isNaN(as)){ alert('请输入有效的比分数字！'); return; }
  await fetch('/api/match/teams', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:editingMatchId,home:home||null,away:away||null})});
  var r = await fetch('/api/match', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:editingMatchId,home_score:hs,away_score:as,home_pen:hp,away_pen:ap})});
  if(r.ok){
    var rr = await fetch('/api/matches'); matchData = await rr.json();
    renderAll(); closeModal();
  } else { alert('保存失败，请重试！'); }
}
async function fillR32(){
  if(!standingsData) return alert('暂无小组赛数据，无法自动填充');
  var gw = ['A','B','C','D','E','F','G','H','I','J','K','L'].map(function(g){
    var rows = standingsData[g]; return rows && rows.length>0 ? rows[0].team : null;
  });
  var pairs = [
    {id:'M1',home:gw[0]},{id:'M3',home:gw[1]},{id:'M5',home:gw[2]},{id:'M6',home:gw[3]},
    {id:'M7',home:gw[4]},{id:'M9',home:gw[5]},{id:'M10',home:gw[6]},{id:'M11',home:gw[7]},
    {id:'M13',home:gw[8]},{id:'M15',home:gw[9]}
  ];
  var cnt = 0;
  for(var i=0; i<pairs.length; i++){
    var p = pairs[i];
    var m = matchData.matches.find(function(x){ return x.id === p.id; });
    if(m && p.home && !m.home){
      await fetch('/api/match/teams', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:p.id,home:p.home})});
      cnt++;
    }
  }
  var rr = await fetch('/api/matches'); matchData = await rr.json();
  renderAll();
  alert('已自动填充 ' + cnt + ' 场32强比赛的小组第一队伍！\n\n其余对阵（部分小组第二的对决、最佳第三名对阵）请手动选择。');
}
async function resetBracket(){
  if(!confirm('确定要重置所有淘汰赛比分和晋级结果吗？此操作不可撤销！')) return;
  await fetch('/api/reset', {method:'POST'});
  var rr = await fetch('/api/matches'); matchData = await rr.json();
  renderAll();
}

// ── 国旗映射 ──
var FLAGS = {
  Brazil:'',Argentina:'',France:'',England:'',Germany:'',Spain:'',Portugal:'',Netherlands:'',
  Belgium:'',Croatia:'',Switzerland:'',Uruguay:'',Colombia:'',Mexico:'',
  'United States':'',USA:'',Japan:'','South Korea':'',Australia:'',Iran:'',
  Morocco:'',Senegal:'',Egypt:'',Austria:'','Czech Republic':'',Turkey:'',Sweden:'',
  Ecuador:'',Paraguay:'','Saudi Arabia':'',Qatar:'','Ivory Coast':'',Ghana:'',
  Tunisia:'',Algeria:'','DR Congo':'','Cape Verde':'',Uzbekistan:'',Jordan:'',
  Panama:'',Haiti:'',Canada:'','New Zealand':'',Norway:'','South Africa':'',
  Iraq:'','Curaçao':'','Bosnia and Herzegovina':'',Scotland:''
};
function getFlag(team){ return ''; }

// ── 中文队名 ──
var CN = {
  Brazil:'巴西',Argentina:'阿根廷',France:'法国',England:'英格兰',Germany:'德国',Spain:'西班牙',
  Portugal:'葡萄牙',Netherlands:'荷兰',Belgium:'比利时',Croatia:'克罗地亚',Switzerland:'瑞士',
  Uruguay:'乌拉圭',Colombia:'哥伦比亚',Mexico:'墨西哥','United States':'美国',USA:'美国',
  Japan:'日本','South Korea':'韩国',Australia:'澳大利亚',Iran:'伊朗',Morocco:'摩洛哥',
  Senegal:'塞内加尔',Egypt:'埃及',Austria:'奥地利','Czech Republic':'捷克',Turkey:'土耳其',
  Sweden:'瑞典',Ecuador:'厄瓜多尔',Paraguay:'巴拉圭','Saudi Arabia':'沙特',Qatar:'卡塔尔',
  'Ivory Coast':'科特迪瓦',Ghana:'加纳',Tunisia:'突尼斯',Algeria:'阿尔及利亚','DR Congo':'刚果(金)',
  'Cape Verde':'佛得角',Uzbekistan:'乌兹别克',Jordan:'约旦',Panama:'巴拿马',Haiti:'海地',
  Canada:'加拿大','New Zealand':'新西兰',Norway:'挪威','South Africa':'南非',Iraq:'伊拉克',
  'Curaçao':'库拉索','Bosnia and Herzegovina':'波黑',Scotland:'苏格兰'
};
function cn(name){ return CN[name] || name; }

document.getElementById('modal').addEventListener('click', function(e){ if(e.target === this) closeModal(); });

init();
