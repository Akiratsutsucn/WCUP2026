import re, json

# Parse Group A match results
with open('E:/Workspace/Kun/WCUP2026/wiki_groups.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find match score patterns - Wikipedia uses football box templates
# Pattern: Team A [[File:flag.png|...]] Team A name ... score ... Team B name ... Team B flag
# Look for score patterns like "1–0" or "2–1"

# Find all football box scores
scores = re.findall(r'(\d+)–(\d+)', html)
print(f"Found {len(scores)} score pairs")
for s in scores[:20]:
    print(f"  {s[0]}-{s[1]}")

# Also find team names near scores
# Wikipedia format: {{fb|BRA}} or [[Brazil national football team|Brazil]]
teams = re.findall(r'title="([^"]+ national football team)"', html)
print(f"\nFound {len(teams)} team mentions:")
for t in set(teams)[:10]:
    print(f"  {t}")

# Try to extract structured match data
# Look for the match result tables
matches = re.findall(r'<div[^>]*class="[^"]*footballbox[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', html, re.DOTALL)
print(f"\nMatch boxes found: {len(matches)}")
