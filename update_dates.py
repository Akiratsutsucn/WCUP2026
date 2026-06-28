import json

with open('E:/Workspace/Kun/WCUP2026/data/matches.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# R32 match schedule (Beijing time)
schedule = {
    'M1':  '6/29 03:00',
    'M2':  '6/30 01:00',
    'M3':  '6/30 04:30',
    'M4':  '6/30 09:00',
    'M5':  '7/1 01:00',
    'M6':  '7/1 05:00',
    'M7':  '7/1 09:00',
    'M8':  '7/2 00:00',
    'M9':  '7/2 04:00',
    'M10': '7/2 08:00',
    'M11': '7/3 03:00',
    'M12': '7/3 07:00',
    'M13': '7/3 11:00',
    'M14': '7/4 02:00',
    'M15': '7/4 06:00',
    'M16': '7/4 09:30',
}

for m in data['matches']:
    if m['id'] in schedule:
        m['date'] = schedule[m['id']]

with open('E:/Workspace/Kun/WCUP2026/data/matches.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Dates updated')

# Also fix the bracket SVG to show dates
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add date display in bracket SVG
# Find the away text line and add date after it
old = "svg += '<line x1=\"' + (p.x+4) + '\" y1=\"' + (p.y+BOX_H/2) + '\" x2=\"' + (p.x+BOX_W-4) + '\" y2=\"' + (p.y+BOX_H/2) + '\" stroke=\"#1a3050\" stroke-width=\"1\"/>';"
new = """svg += '<line x1=\"' + (p.x+4) + '\" y1=\"' + (p.y+BOX_H/2) + '\" x2=\"' + (p.x+BOX_W-4) + '\" y2=\"' + (p.y+BOX_H/2) + '\" stroke=\"#1a3050\" stroke-width=\"1\"/>';
    if(m.date) svg += '<text x=\"' + (p.x+BOX_W/2) + '\" y=\"' + (p.y+BOX_H+10) + '\" fill=\"#7aa4c8\" font-size=\"8\" text-anchor=\"middle\">' + m.date + '</text>';"""

html = html.replace(old, new)
with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Frontend updated')
