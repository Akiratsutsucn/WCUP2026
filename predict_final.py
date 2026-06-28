import json, math, random

# Load data
with open('E:/Workspace/Kun/WCUP2026/data/team_profiles.json', 'r', encoding='utf-8') as f:
    profiles = json.load(f)
with open('E:/Workspace/Kun/WCUP2026/data/elo_cache_2026.json', 'r', encoding='utf-8') as f:
    elo_cache = json.load(f)

def get_elo(team):
    v = elo_cache.get(team, 1700)
    return float(v) if not isinstance(v, dict) else float(v.get('elo', 1700))

# R32 matchups
matches = [
    ("South Africa", "Canada"),
    ("Brazil", "Japan"),
    ("Germany", "Paraguay"),
    ("Netherlands", "Morocco"),
    ("Ivory Coast", "Norway"),
    ("France", "Sweden"),
    ("Mexico", "Ecuador"),
    ("England", "DR Congo"),
    ("Belgium", "Senegal"),
    ("United States", "Bosnia and Herzegovina"),
    ("Spain", "Austria"),
    ("Portugal", "Croatia"),
    ("Switzerland", "Algeria"),
    ("Australia", "Egypt"),
    ("Argentina", "Cape Verde"),
    ("Colombia", "Ghana"),
]

print("=" * 60)
print("2026 WCUP R32 综合预测（Elo + 小组赛表现 + 攻防数据）")
print("=" * 60)
print(f"{'比赛':<30} {'比分':>6} {'胜':>6} {'平':>6} {'负':>6}")
print("-" * 60)

for team_a, team_b in matches:
    elo_a = get_elo(team_a)
    elo_b = get_elo(team_b)
    elo_diff = elo_a - elo_b
    
    pa = profiles.get(team_a, {})
    pb = profiles.get(team_b, {})
    
    # Form factor (0-1 scale from group stage points)
    form_a = pa.get('pts_per_game', 2.0) / 3.0
    form_b = pb.get('pts_per_game', 2.0) / 3.0
    
    # Goal difference quality (normalized)
    gd_a = max(-1.5, min(1.5, pa.get('gd_per_game', 0)))
    gd_b = max(-1.5, min(1.5, pb.get('gd_per_game', 0)))
    
    # Composite strength score (Elo dominant, form/gd as modifiers)
    elo_score_a = (elo_a - 1700) / 300.0
    elo_score_b = (elo_b - 1700) / 300.0
    strength_a = elo_score_a * 0.6 + form_a * 0.2 + gd_a * 0.2
    strength_b = elo_score_b * 0.6 + form_b * 0.2 + gd_b * 0.2
    
    # Expected goals
    base = 1.05
    lambda_a = base + strength_a * 0.4
    lambda_b = base + strength_b * 0.4
    lambda_a = max(0.3, min(2.5, lambda_a))
    lambda_b = max(0.3, min(2.5, lambda_b))
    
    # Win probability
    expected = 1.0 / (1.0 + math.pow(10, -elo_diff / 400.0))
    draw_p = max(0.10, min(0.28, 0.26 * math.exp(-abs(elo_diff) / 500.0)))
    win_a = (1.0 - draw_p) * expected
    win_b = (1.0 - draw_p) * (1.0 - expected)
    
    # Most likely score (Poisson mode)
    pred_h = int(lambda_a)
    pred_a = int(lambda_b)
    if lambda_a - pred_h > 0.5: pred_h += 1
    if lambda_b - pred_a > 0.5: pred_a += 1
    pred_h = max(0, pred_h)
    pred_a = max(0, pred_a)
    
    print(f"{team_a:<15} vs {team_b:<15} {pred_h}-{pred_a}  {win_a*100:5.1f}% {draw_p*100:5.1f}% {win_b*100:5.1f}%")

print("-" * 60)
print("模型: Poisson进球分布 × Elo(60%) + 小组赛表现(20%) + 净胜球(20%)")
