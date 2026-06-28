with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'r', encoding='utf-8') as f:
    e = f.read()

old_start = e.find('def predict_h2h(team_a, team_b):')
old_end = e.find('\ndef get_injury_impact(')
if old_start > 0 and old_end > old_start:
    new_func = '''def predict_h2h(team_a, team_b):
    import math
    score_a = compute_team_score(team_a)
    score_b = compute_team_score(team_b)
    elo_a = score_a.get("elo", 1700) if isinstance(score_a, dict) else 1700
    elo_b = score_b.get("elo", 1700) if isinstance(score_b, dict) else 1700
    elo_diff = elo_a - elo_b
    expected_a = 1.0 / (1.0 + math.pow(10, -elo_diff / 400.0))
    expected_b = 1.0 - expected_a
    abs_diff = abs(elo_diff)
    draw_prob = 0.28 * math.exp(-abs_diff / 600.0)
    draw_prob = max(0.08, min(0.30, draw_prob))
    p_a = (1.0 - draw_prob) * expected_a
    p_b = (1.0 - draw_prob) * expected_b
    base_goals = 1.35
    adj_a = max(0.4, min(2.5, 0.7 + elo_diff / 1500.0))
    adj_b = max(0.4, min(2.5, 0.7 - elo_diff / 1500.0))
    lambda_a = base_goals * adj_a
    lambda_b = base_goals * adj_b
    pred_home = max(0, round(lambda_a))
    pred_away = max(0, round(lambda_b))
    return {"team_a":team_a,"team_b":team_b,"elo_a":round(elo_a),"elo_b":round(elo_b),
            "elo_diff":round(elo_diff),"win_prob_a":round(p_a*100,1),
            "draw_prob":round(draw_prob*100,1),"win_prob_b":round(p_b*100,1),
            "expected_goals_a":round(lambda_a,2),"expected_goals_b":round(lambda_b,2),
            "predicted_score":str(pred_home)+"-"+str(pred_away)}
'''
    e = e[:old_start] + new_func + '\n' + e[old_end:]
    with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'w', encoding='utf-8') as f:
        f.write(e)
    print('H2H function replaced')
else:
    print('Not found:', old_start, old_end)
