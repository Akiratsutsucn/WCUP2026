$f = Get-Content 'static\index.html' -Raw -Encoding UTF8

# Predict tab: team name in display
$f = $f -replace "`"`" \+ t\.team \+ `"</span>`"", "`"`" + cn(t.team) + `"</span>`""

# H2H team_a display
$f = $f -replace "t_team_a", "t_team_a_cn"  # placeholder to avoid partial matches

$f | Out-File 'static\index.html' -Encoding UTF8 -NoNewline
Write-Host "Done"
