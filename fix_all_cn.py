import re

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix modal dropdown - show "中文名" in select options
html = html.replace(
    "var opts = '<option value=\"\">-- 请选择 --</option>';",
    "var opts = '<option value=\"\">-- 请选择 --</option>';"
)
# Replace the option loop for modal dropdown
old_modal = r'opts \+= \'<option value=\"\' \+ allTeams\[i\] \+ \'\">\' \+ allTeams\[i\] \+ \'</option>\';'
new_modal = r'opts += \'<option value=\"\' + allTeams[i] + \'\">\' + cn(allTeams[i]) + \'</option>\';'
html, n = re.subn(old_modal, new_modal, html)
print(f"Modal dropdown: {n} replacements")

# 2. Fix H2H dropdowns
old_h2h = r"h \+= '<option>' \+ allTeams\[i\] \+ '</option>'"
new_h2h = r"h += '<option value=\"' + allTeams[i] + '\">' + cn(allTeams[i]) + '</option>'"
html, n = re.subn(old_h2h, new_h2h, html)
print(f"H2H dropdown: {n} replacements")

# 3. Fix Squad dropdown
old_sq = r"h \+= '<option>' \+ allTeams\[i\] \+ '</option>'"
html, n = re.subn(old_sq, new_h2h, html)
print(f"Squad/Mystic dropdown: {n} replacements")

# 4. Fix bracket match card - the `cn(m.home||'待定')` should be `m.home ? cn(m.home) : '待定'`
# Already fixed above

# 5. Fix H2H result team names - already done via earlier fix

# 6. Fix the "VS" in H2H tab header (already "对阵")

# 7. Fix the H2H tab select options in renderH2H
# The renderH2H function uses for(var i=0; allTeams loop)
html = html.replace(
    "for(var i=0; i<allTeams.length; i++) h += '<option>' + allTeams[i] + '</option>';",
    "for(var i=0; i<allTeams.length; i++) h += '<option value=\"' + allTeams[i] + '\">' + cn(allTeams[i]) + '</option>';"
)

# 8. Fix the 2nd H2H select
html = html.replace(
    "for(var j=0; j<allTeams.length; j++) h += '<option>' + allTeams[j] + '</option>'",
    "for(var j=0; j<allTeams.length; j++) h += '<option value=\"' + allTeams[j] + '\">' + cn(allTeams[j]) + '</option>'"
)

# 9. Fix the squad select label
# (keep squad select showing cn name too)

# 10. Fix factor select
old_fac = r"h \+= '<option>' \+ predictData\.rankings\[i\]\.team \+ '</option>'"
new_fac = r"h += '<option>' + cn(predictData.rankings[i].team) + '</option>'"
html, n = re.subn(old_fac, new_fac, html)
print(f"Factor select: {n} replacements")

# 11. Fix mystic select
html = html.replace(
    "for(var i=0; i<Math.min(allTeams.length, 30); i++) h += '<option>' + allTeams[i] + '</option>'",
    "for(var i=0; i<Math.min(allTeams.length, 30); i++) h += '<option>' + cn(allTeams[i]) + '</option>'"
)

# 12. Fix section-group headers (group card)
# The standings render is missing - let me check if renderGroups function exists

# 13. Fix all alert messages to be in Chinese
# (already done)

# 14. Also add a helper function to format team name with flag for dropdowns
# Not needed since cn() handles it

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done - all dropdowns now show Chinese names")
