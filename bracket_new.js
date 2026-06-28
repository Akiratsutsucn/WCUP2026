// ── 7. 淘汰赛对阵 ──
function renderBracketPage(){
  var h = '<div class=\"card\"><h3>🏟 淘汰赛对阵图 — 32强 → 决赛</h3>';
  h += '<div class=\"btn-bar\"><button class=\"btn-sm\" onclick=\"fillR32()\">🔄 自动填充32强</button><button class=\"btn-sm\" onclick=\"resetBracket()\" style=\"background:#5a3030;color:#e88;\">⚠ 重置全部比赛</button></div>';
  h += '<div id=\"bracket-svg-container\" style=\"overflow-x:auto;\"></div>';
  h += '</div>';
  setTimeout(function(){ drawBracketSVG(); }, 150);
  return h;
}

function drawBracketSVG(){
  if(!matchData || !matchData.matches) return;
  var ms = matchData.matches;
  var matchById = {}; ms.forEach(function(m){ matchById[m.id] = m; });
  
  var rounds = ['R32','R16','QF','SF','F','3rd'];
  var labels = ['32强','16强','\\u00bc决赛','半决赛','🏆 决赛','季军赛'];
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
  
  var svg = '<svg width=\"' + svgW + '\" height=\"' + maxY + '\" style=\"background:#0a0f1a;font-family:system-ui,sans-serif;\">';
  
  // Connector lines
  svg += '<g stroke=\"#c9a84c\" stroke-width=\"2\" fill=\"none\" opacity=\"0.6\">';
  for(var mid in pos){
    var m = matchById[mid]; if(!m || !m.next) continue;
    var p1 = pos[mid], p2 = pos[m.next]; if(!p1 || !p2) continue;
    var x1 = p1.x + BOX_W, y1 = p1.y + BOX_H/2;
    var x2 = p2.x, y2 = p2.y + BOX_H/2;
    var mx = (x1 + x2) / 2;
    svg += '<path d=\"M' + x1 + ',' + y1 + ' L' + mx + ',' + y1 + ' L' + mx + ',' + y2 + ' L' + x2 + ',' + y2 + '\"/>';
  }
  // 3rd place dashed lines from SF losers
  if(tpm && sf.length>=2){
    for(var i=0; i<2; i++){
      var sx = pos[sf[i].id].x + BOX_W, sy = pos[sf[i].id].y + BOX_H*0.75;
      var tx = pos[tpm.id].x, ty = pos[tpm.id].y + BOX_H/2;
      var mx2 = sx + 25;
      svg += '<path d=\"M' + sx + ',' + sy + ' L' + mx2 + ',' + sy + ' L' + mx2 + ',' + ty + ' L' + tx + ',' + ty + '\" stroke=\"#a08040\" stroke-dasharray=\"5,3\"/>';
    }
  }
  svg += '</g>';
  
  // Round titles
  svg += '<g fill=\"#f0d878\" font-size=\"12\" font-weight=\"bold\" text-anchor=\"middle\">';
  for(var i=0; i<rounds.length; i++)
    svg += '<text x=\"' + (X[i] + BOX_W/2) + '\" y=\"14\">' + labels[i] + '</text>';
  svg += '</g>';
  
  // Match boxes
  for(var mid in pos){
    var p = pos[mid], m = matchById[mid]; if(!m) continue;
    var home = m.home ? cn(m.home) : '待定', away = m.away ? cn(m.away) : '待定';
    var hs = m.home_score!=null ? m.home_score : '-', as = m.away_score!=null ? m.away_score : '-';
    var hw = m.winner==='home', aw = m.winner==='away';
    var fill = m.winner ? '#0a1a10' : '#0f1a2e', border = m.winner ? '#2a5a30' : '#1a3050';
    
    svg += '<g onclick=\"openModal(\\'' + mid + '\\')\" style=\"cursor:pointer\">';
    svg += '<rect x=\"' + p.x + '\" y=\"' + p.y + '\" width=\"' + BOX_W + '\" height=\"' + BOX_H + '\" rx=\"6\" fill=\"' + fill + '\" stroke=\"' + border + '\" stroke-width=\"1.5\"/>';
    svg += '<text x=\"' + (p.x+6) + '\" y=\"' + (p.y+18) + '\" fill=\"' + (hw?'#f0d878':'#c0c8d8') + '\" font-size=\"11\" font-weight=\"' + (hw?'bold':'normal') + '\">' + home.substring(0,14) + '</text>';
    svg += '<text x=\"' + (p.x+BOX_W-6) + '\" y=\"' + (p.y+18) + '\" fill=\"#f0d878\" font-size=\"11\" font-weight=\"bold\" text-anchor=\"end\">' + hs + '</text>';
    svg += '<line x1=\"' + (p.x+4) + '\" y1=\"' + (p.y+BOX_H/2) + '\" x2=\"' + (p.x+BOX_W-4) + '\" y2=\"' + (p.y+BOX_H/2) + '\" stroke=\"#1a3050\" stroke-width=\"1\"/>';
    svg += '<text x=\"' + (p.x+6) + '\" y=\"' + (p.y+40) + '\" fill=\"' + (aw?'#f0d878':'#c0c8d8') + '\" font-size=\"11\" font-weight=\"' + (aw?'bold':'normal') + '\">' + away.substring(0,14) + '</text>';
    svg += '<text x=\"' + (p.x+BOX_W-6) + '\" y=\"' + (p.y+40) + '\" fill=\"#f0d878\" font-size=\"11\" font-weight=\"bold\" text-anchor=\"end\">' + as + '</text>';
    svg += '</g>';
  }
  
  svg += '</svg>';
  document.getElementById('bracket-svg-container').innerHTML = svg;
}
