"""
WCUP2026 预测引擎 — 整合球员评分、球队评分、实力、蒙特卡洛、玄学、UCL信号
从 reference_project 移植，适配 Flask 后端
"""
import json
import os
import sys
import math
import random
from pathlib import Path

import numpy as np

# 路径
ENGINE_DIR = Path(__file__).parent
PROJECT_DIR = ENGINE_DIR.parent
DATA_DIR = PROJECT_DIR / 'data'

# 加载数据文件
def _load_json(name):
    with open(DATA_DIR / name, 'r', encoding='utf-8') as f:
        return json.load(f)

PLAYERS_DATA = _load_json('wc2026_players_processed.json')
ELO_CACHE = _load_json('elo_cache_2026.json')
MATCH_CACHE = _load_json('match_cache.json')
# 加载中文队名映射
try:
    TEAM_NAMES_CN = _load_json('team_names_cn.json')
    CN_PLAYERS = _load_json('cn_players_en.json')
except:
    TEAM_NAMES_CN = {}
    CN_PLAYERS = {}

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

def cn(team_name):
    """返回球队中文名，如果没有映射则返回英文原名"""
    return TEAM_NAMES_CN.get(team_name, team_name)

# ── 球队名称标准化 ─────────────────────────────────────
TEAM_NAME_NORMALIZE = {
    'USA': 'United States', 'South Korea': 'South Korea',
    'Ivory Coast': "Côte d'Ivoire", 'Cape Verde': 'Cape Verde',
    'Curaçao': 'Curaçao', 'Czech Republic': 'Czech Republic',
    'Bosnia and Herzegovina': 'Bosnia and Herzegovina',
}

# ── 实力 数据 ──────────────────────────────────────────
def get_elo(team_name):
    """获取球队 实力 评分"""
    for k, v in ELO_CACHE.items():
        if k.lower() == team_name.lower() or team_name.lower() in k.lower():
            if isinstance(v, dict):
                return v.get('elo', 1700)
            return float(v)
    return 1700

def get_all_elos():
    result = {}
    for k, v in ELO_CACHE.items():
        result[k] = v.get('elo', 1700)
    return result

# ── 球队名称标准化映射 ──────────────────────────────
TEAM_ALIASES = {
    'United States': 'USA', 'USA': 'USA',
    'South Korea': 'South Korea', 'Korea Republic': 'South Korea',
    'Ivory Coast': "Cote d'Ivoire", "Cote d'Ivoire": "Cote d'Ivoire",
    'Czech Republic': 'Czech Republic', 'Czechia': 'Czech Republic',
    'Bosnia and Herzegovina': 'Bosnia and Herzegovina',
    'Cape Verde': 'Cape Verde',
    'Curacao': 'Curacao', 'Curaçao': 'Curacao',
}

def _normalize_team(name):
    """统一球队名称"""
    if name in TEAM_ALIASES:
        return TEAM_ALIASES[name]
    return name

# ── 球员数据 ──────────────────────────────────────────
def get_team_players(team_name):
    """获取某队球员列表"""
    teams = PLAYERS_DATA.get('teams', PLAYERS_DATA)
    # 直接匹配
    if team_name in teams:
        v = teams[team_name]
        return v.get('players', v) if isinstance(v, dict) else (v if isinstance(v, list) else [])
    # 别名匹配
    alias = _normalize_team(team_name)
    if alias != team_name and alias in teams:
        v = teams[alias]
        return v.get('players', v) if isinstance(v, dict) else (v if isinstance(v, list) else [])
    # 小写匹配
    tn_lower = team_name.lower()
    for k, v in teams.items():
        if k.lower() == tn_lower or tn_lower in k.lower() or k.lower() in tn_lower:
            return v.get('players', v) if isinstance(v, dict) else (v if isinstance(v, list) else [])
    return []

def get_team_player_count(team_name):
    return len(get_team_players(team_name))

# ── 伤病与停赛数据 ────────────────────────────────────
def load_injuries_suspensions():
    """加载伤病和停赛数据（从 matches cache 推算或手动补充）"""
    path = DATA_DIR / 'injuries_suspensions.json'
    if path.exists():
        return _load_json('injuries_suspensions.json')
    return {}

def save_injuries_suspensions(data):
    with open(DATA_DIR / 'injuries_suspensions.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── 球队评分（简化版，直接调用 team_scoring） ──────────
def compute_team_score(team_name):
    """计算球队综合评分"""
    elo = get_elo(team_name)
    players = get_team_players(team_name)
    player_count = len(players)

    # 年龄结构评分（简化）
    if players:
        ages = []
        for p in players:
            age = p.get('age', 27)
            if isinstance(age, (int, float)) and 16 < age < 45:
                ages.append(age)
        if ages:
            avg_age = sum(ages) / len(ages)
            median_age = sorted(ages)[len(ages) // 2]
            # 黄金年龄 25-29
            age_score = max(0, 1.0 - abs(median_age - 27) / 15)
        else:
            age_score = 0.6
            avg_age = 27
    else:
        age_score = 0.6
        avg_age = 27

    # 大赛经验评分
    experienced = 0
    for p in players:
        caps = p.get('caps', 0)
        if isinstance(caps, (int, float)) and caps >= 20:
            experienced += 1
    exp_ratio = experienced / max(1, player_count)
    experience_score = min(1.0, exp_ratio * 2.5)

    # 综合评分（实力锚点主导）
    normalized_elo = (elo - 1500) / 700  # ~0到1
    normalized_elo = max(0, min(1, normalized_elo))

    total_score = (
        normalized_elo * 0.40 +
        age_score * 0.25 +
        experience_score * 0.20 +
        0.15  # baseline
    )
    return {
        'team': team_name,
        'elo': elo,
        'player_count': player_count,
        'avg_age': round(avg_age, 1) if players else None,
        'age_score': round(age_score, 3),
        'experience_score': round(experience_score, 3),
        'total_score': round(total_score, 4),
        'normalized_elo': round(normalized_elo, 4),
    }

def compute_all_team_scores():
    """计算所有48队评分并排名"""
    teams_data = _load_json('teams.json')
    all_teams = []
    for g in teams_data.get('groups', {}).values():
        for t in g:
            all_teams.append(t['team'])

    results = []
    for team in all_teams:
        try:
            score = compute_team_score(team)
            results.append(score)
        except Exception as e:
            results.append({'team': team, 'error': str(e)})

    results.sort(key=lambda x: x.get('total_score', 0), reverse=True)
    return results

# ── 玄学因子 ──────────────────────────────────────────
def compute_mystic_factor(team_name, elo=None):
    """计算玄学因子（简化版，核心逻辑）"""
    if elo is None:
        elo = get_elo(team_name)

    # 强势方诅咒（实力越高压力越大）
    favorite_curse = -0.03 * (elo - 1750) / 400 if elo > 1750 else 0

    # 东道主优势
    hosts = ['United States', 'Canada', 'Mexico']
    host_bonus = 0.05 if team_name in hosts else 0

    # 卫冕冠军诅咒
    defending_champ_curse = -0.04 if team_name == 'Argentina' else 0

    # 新势力崛起
    new_force_bonus = 0.03 if elo < 1650 else 0

    # 运气成分（固定种子）
    rng = random.Random(hash(team_name) % 10000)
    luck = rng.uniform(-0.03, 0.08)

    total_mystic = favorite_curse + host_bonus + defending_champ_curse + new_force_bonus + luck
    total_mystic = max(-0.15, min(0.15, total_mystic))

    return {
        'team': team_name,
        'favorite_curse': round(favorite_curse, 4),
        'host_bonus': round(host_bonus, 4),
        'defending_champ_curse': round(defending_champ_curse, 4),
        'new_force_bonus': round(new_force_bonus, 4),
        'luck': round(luck, 4),
        'total_mystic': round(total_mystic, 4),
    }

# ── 玄学详情分析（供前端展示） ──────────────────────
def compute_team_mystic(team_name):
    try:
        elo = get_elo(team_name) or 1700
        mf = compute_mystic_factor(team_name, elo)
        score = compute_team_score(team_name)
        if not isinstance(score, dict): score = {'total_score':0.5,'avg_age':None,'player_count':0,'experience_score':0}
        logical_prob = score.get('total_score', 0.5)
        avg_age = score.get('avg_age', None)
        player_count = score.get('player_count', 0)
        exp_score = score.get('experience_score', 0)
        is_host = team_name in ['United States','Canada','Mexico']
        is_defending = team_name == 'Argentina'
        
        # Stage 1: varied based on actual score
        if logical_prob > 0.85: s1 = cn(team_name)+"综合实力顶级，是本届冠军最有力争夺者之一。实力评分"+str(round(elo))+"，阵容深度与球星个人能力兼备。"
        elif logical_prob > 0.75: s1 = cn(team_name)+"整体实力强劲，具备冲击四强的资本。实力评分"+str(round(elo))+"，攻防体系成熟。"
        elif logical_prob > 0.65: s1 = cn(team_name)+"战力处于中上游，淘汰赛签运将很大程度决定能走多远。实力"+str(round(elo))+"。"
        elif logical_prob > 0.55: s1 = cn(team_name)+"属于中游球队，需要在关键比赛超常发挥才能突破。实力"+str(round(elo))+"。"
        elif logical_prob > 0.45: s1 = cn(team_name)+"实力偏弱，但世界杯历史上从不缺少黑马。实力"+str(round(elo))+"。"
        else: s1 = cn(team_name)+"纸面实力不占优，但不被看好反而可能成为最大优势。实力"+str(round(elo))+"。"
        
        # Stage 2: actual biases
        biases = []
        if abs(mf.get('favorite_curse',0)) > 0.01: biases.append("强势方诅咒")
        if mf.get('host_bonus',0) > 0: biases.append("东道主加成")
        if mf.get('defending_champ_curse',0) < -0.01: biases.append("卫冕压力")
        if mf.get('new_force_bonus',0) > 0: biases.append("新势力红利")
        if avg_age and avg_age < 25: biases.append("年轻缺乏经验")
        if avg_age and avg_age > 30: biases.append("阵容老化风险")
        if player_count < 15: biases.append("阵容深度不足")
        if not biases: biases.append("无明显数据偏差")
        s2 = "数据偏差："+"、".join(biases)
        
        # Stage 3: specific to team situation
        if is_defending: s3 = cn(team_name)+"是卫冕冠军。历史上能做到连续夺冠的球队屈指可数，压力与荣耀并存。"
        elif is_host: s3 = cn(team_name)+"作为东道主，拥有主场之利。但东道主在淘汰赛阶段的心理压力同样不容忽视。"
        elif elo > 1880: s3 = cn(team_name)+"拥有顶级战力，真正的考验在于淘汰赛的心理素质——越是强队，越容易被针对研究。"
        elif elo > 1800: s3 = cn(team_name)+"强队底蕴深厚，但夺冠需要天时地利人和的完美结合。"
        elif elo > 1700 and avg_age and avg_age < 26: s3 = cn(team_name)+"年轻有冲劲，体能充沛是淘汰赛的隐形优势。欠缺的是大赛关键时刻的经验。"
        elif elo < 1650: s3 = cn(team_name)+"实力不占优，但足球的魅力正在于此——弱者在绝境中往往能激发出超乎想象的能量。"
        elif avg_age and avg_age < 26: s3 = cn(team_name)+"青春风暴席卷而来，年轻人不知畏惧为何物，这正是淘汰赛最可怕的武器。"
        elif exp_score > 0.6: s3 = cn(team_name)+"大赛经验丰富，老将们在关键时刻的冷静判断是球队的定海神针。"
        else: s3 = cn(team_name)+"每支球队都有自己的命运。淘汰赛不看排名看临场，一切皆有可能。"
        
        # Tao - more varied
        if elo > 1880: tao = "「反者道之动」——盛极必衰。"+cn(team_name)+"强到极点，反而最脆弱。保持谦逊比展现强大更重要。"
        elif elo > 1800: tao = "「大巧若拙」——真正的强队不需要场场碾压，懂得在关键时刻发力才是智慧。"
        elif elo < 1600: tao = "「柔弱胜刚强」——不被看好反而是最大的自由。没有包袱，放手一搏。"
        elif avg_age and avg_age < 25: tao = "「含德之厚，比于赤子」——年轻球队如婴儿般纯真无畏，这种状态最接近道。"
        elif avg_age and avg_age > 30: tao = "「大器晚成」——经验是最好的老师，老将的沉稳能化解任何风暴。"
        else: tao = "「道法自然」——不强行逆势，顺势而为。淘汰赛的每一步都需顺应天时。"
        
        # I Ching - more varied
        if is_host: gua = "泰卦——天地交融，上下同心。东道主占据天时地利人和。"
        elif is_defending: gua = "否卦——天地闭塞。卫冕之路布满荆棘，需要打破内外桎梏。"
        elif elo > 1880: gua = "乾卦九五——飞龙在天。但上九'亢龙有悔'警示：巅峰之后便是下坡。"
        elif elo > 1800: gua = "大有卦——顺天应时。拥有足够的实力，关键在于把握时机。"
        elif elo < 1600: gua = "复卦——一阳来复。在最不被看好的低谷，恰恰是反弹的开始。"
        elif avg_age and avg_age < 25: gua = "震卦——雷声震动。年轻球队如春雷般充满爆发力与不确定性。"
        elif avg_age and avg_age > 30: gua = "艮卦——如山静止。老将如磐石，在风暴中岿然不动。"
        elif exp_score > 0.5: gua = "既济卦——事已成就但需谨慎守成。经验丰富但不可掉以轻心。"
        elif elo > 1700: gua = "离卦——光明依附。需要核心球员的带领才能发挥最大战力。"
        else: gua = "屯卦——万物初生。起步维艰但充满无限可能，淘汰赛正是破茧之时。"
        
        return {'team':team_name,'team_cn':cn(team_name),'elo':elo,
                'three_stages':{'stage1':s1,'stage2':s2,'stage3':s3},
                'tao_te_ching':tao,'i_ching':gua,'mystic_factors':mf}
    except Exception as ex:
        return {'team':team_name,'team_cn':cn(team_name),'error':str(ex)}

def compute_all_mystic():
    """计算所有球队的玄学摘要"""
    scores = compute_all_team_scores()
    result = {}
    for s in scores[:20]:
        team = s['team']
        result[team] = compute_team_mystic(team)
    return result

# ── 冠军概率预测 ──────────────────────────────────────
def predict_champion_probabilities():
    """基于实力的冠军概率预测（简化蒙特卡洛）"""
    scores = compute_all_team_scores()
    total = sum(s['total_score'] for s in scores if 'total_score' in s)
    
    results = []
    for s in scores:
        if 'total_score' not in s:
            continue
        prob = s['total_score'] / total if total > 0 else 0
        mystic = compute_mystic_factor(s['team'], s.get('elo', 1700))
        # 玄学调整
        adjusted_prob = prob * (1 + mystic['total_mystic'])
        
        results.append({
            'team': s['team'],
            'elo': s['elo'],
            'raw_prob': round(prob * 100, 2),
            'mystic_adjustment': round(mystic['total_mystic'] * 100, 2),
            'adjusted_prob': round(adjusted_prob / sum(r.get('adjusted_prob', 0) if 'adjusted_prob' in r else 0 for r in []) * 100 if False else adjusted_prob * 100, 2),
            'score': s['total_score'],
            'player_count': s['player_count'],
            'avg_age': s['avg_age'],
        })
    
    # Normalize adjusted probabilities
    total_adj = sum(r['adjusted_prob'] for r in results)
    for r in results:
        r['adjusted_prob'] = round(r['adjusted_prob'] / total_adj * 100, 2) if total_adj > 0 else 0
    
    results.sort(key=lambda x: x['adjusted_prob'], reverse=True)
    
    # Add rank
    for i, r in enumerate(results):
        r['rank'] = i + 1
    
    return results

# ── 蒙特卡洛模拟（完整版） ────────────────────────────
def monte_carlo_simulation(num_simulations=10000):
    """蒙特卡洛模拟世界杯淘汰赛"""
    scores = compute_all_team_scores()
    team_scores = {s['team']: s.get('total_score', 0.5) for s in scores if 'total_score' in s}
    
    win_count = {team: 0 for team in team_scores}
    
    # 32强（取评分最高的32队）
    qualified = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)[:32]
    
    rng = np.random.RandomState(RANDOM_SEED)
    
    for _ in range(num_simulations):
        teams = [t[0] for t in qualified]
        # 单淘汰模拟
        while len(teams) > 1:
            next_round = []
            for i in range(0, len(teams), 2):
                t1, t2 = teams[i], teams[i+1]
                s1, s2 = team_scores[t1], team_scores[t2]
                # 概率计算
                p1 = 1 / (1 + math.exp(-(s1 - s2) * 8))
                if rng.random() < p1:
                    next_round.append(t1)
                else:
                    next_round.append(t2)
            teams = next_round
        if teams:
            win_count[teams[0]] += 1
    
    # 排序输出
    results = []
    for team, wins in win_count.items():
        results.append({
            'team': team,
            'wins': wins,
            'probability': round(wins / num_simulations * 100, 2),
        })
    
    results.sort(key=lambda x: x['probability'], reverse=True)
    for i, r in enumerate(results):
        r['rank'] = i + 1
    
    return results

# ── H2H 预测 ──────────────────────────────────────────
def predict_h2h(team_a, team_b):
    import math
    score_a = compute_team_score(team_a)
    score_b = compute_team_score(team_b)
    elo_a = score_a.get("elo", 1700) if isinstance(score_a, dict) else 1700
    elo_b = score_b.get("elo", 1700) if isinstance(score_b, dict) else 1700
    elo_diff = elo_a - elo_b
    abs_diff = abs(elo_diff)
    
    # Win/draw/loss probabilities
    expected_a = 1.0 / (1.0 + math.pow(10, -elo_diff / 400.0))
    draw_prob = max(0.10, min(0.28, 0.26 * math.exp(-abs_diff / 500.0)))
    p_a = round((1.0 - draw_prob) * expected_a * 100, 1)
    p_b = round((1.0 - draw_prob) * (1.0 - expected_a) * 100, 1)
    draw_pct = round(draw_prob * 100, 1)
    
    # Elo-calibrated expected goals (World Cup knockout data)
    # Each 100 Elo points ≈ 0.22 goals advantage
    adj_diff = elo_diff
    # Injury adjustment: each high-impact injury ≈ -60 Elo
    injuries = load_injuries_suspensions()
    inj_a = injuries.get('injuries', {}).get(team_a, [])
    inj_b = injuries.get('injuries', {}).get(team_b, [])
    high_a = sum(1 for i in inj_a if i.get('impact') == 'high')
    high_b = sum(1 for i in inj_b if i.get('impact') == 'high')
    adj_diff = elo_diff - (high_a * 60) + (high_b * 60)
    
    # Expected goals: base 1.05 per team + Elo adjustment
    base = 1.05
    rate = 0.22  # goals per 100 Elo
    lambda_a = base + (adj_diff / 100.0) * rate
    lambda_b = base - (adj_diff / 100.0) * rate
    lambda_a = max(0.15, min(3.5, lambda_a))
    lambda_b = max(0.15, min(3.5, lambda_b))
    
    # Most likely score: Poisson mode for each team
    # P(X=k) = e^(-λ) * λ^k / k! — mode = floor(λ)
    pred_home = int(lambda_a)  # floor
    pred_away = int(lambda_b)
    # Adjust: if fractional part > 0.6, round up
    if lambda_a - pred_home > 0.6: pred_home += 1
    if lambda_b - pred_away > 0.6: pred_away += 1
    pred_home = max(0, pred_home)
    pred_away = max(0, pred_away)
    
    return {"team_a":team_a,"team_b":team_b,"elo_a":round(elo_a),"elo_b":round(elo_b),
            "elo_diff":round(elo_diff),"win_prob_a":p_a,"draw_prob":draw_pct,"win_prob_b":p_b,
            "expected_goals_a":lambda_a,"expected_goals_b":lambda_b,
            "predicted_score":str(pred_home)+"-"+str(pred_away)}


def get_injury_impact(team_name):
    """获取伤病/停赛对球队的影响"""
    data = load_injuries_suspensions()
    team_data = data.get(team_name, {})
    
    injuries = team_data.get('injuries', [])
    suspensions = team_data.get('suspensions', [])
    
    total_impact = 0.0
    for inj in injuries:
        severity = inj.get('severity', 'medium')  # low, medium, high
        is_key = inj.get('key_player', False)
        factor = {'low': 0.01, 'medium': 0.03, 'high': 0.08}[severity]
        if is_key:
            factor *= 1.5
        total_impact += factor
    
    for sus in suspensions:
        is_key = sus.get('key_player', False)
        factor = 0.04 if is_key else 0.02
        total_impact += factor
    
    return {
        'team': team_name,
        'injuries': injuries,
        'injuries_count': len(injuries),
        'suspensions': suspensions,
        'suspensions_count': len(suspensions),
        'total_impact': round(min(0.30, total_impact), 3),
        'adjusted_factor': round(1.0 - min(0.30, total_impact), 3),
    }


# ══════════════════════════════════════════════════════════════
# PredictionEngine — Flask集成接口
# ══════════════════════════════════════════════════════════════


def _get_r32_teams():
    try:
        matches = _load_json("matches.json")
        teams = set()
        for m in matches.get("matches", []):
            if m.get("round") == "R32":
                if m.get("home"): teams.add(m["home"])
                if m.get("away"): teams.add(m["away"])
        return teams
    except:
        return None

class PredictionEngine:
    """预测引擎统一接口"""
    
    def __init__(self):
        self._rankings = None
        self._mystic_summary = None
        self._elo_data = None
        self._ucl_signals = None
        self._init_data()
    
    def _init_data(self):
        try:
            self._rankings = compute_all_team_scores()
            self._mystic_summary = compute_all_mystic() if 'compute_all_mystic' in globals() else {}
            self._elo_data = ELO_CACHE
            self._ucl_signals = compute_ucl_signals() if 'compute_ucl_signals' in globals() else {}
        except Exception as e:
            print(f"[ENGINE] Init warning: {e}")
            self._rankings = []
            self._mystic_summary = {}
            self._elo_data = {}
            self._ucl_signals = {}
    
    def get_rankings(self):
        if not self._rankings:
            self._rankings = compute_all_team_scores()
        # Add probability calculations
        results = []
        total = sum(s.get('total_score', 0) for s in self._rankings if isinstance(s, dict))
        for s in self._rankings:
            if not isinstance(s, dict): continue
            score = s.get('total_score', 0)
            raw_prob = (score / total * 100) if total > 0 else 0
            mystic = compute_mystic_factor(s['team'], s.get('elo', 1700))
            adj = raw_prob * (1 + mystic.get('total_mystic', 0))
            results.append({
                'team': s['team'],
                'elo': s.get('elo', 1700),
                'player_count': s.get('player_count', 0),
                'avg_age': s.get('avg_age'),
                'total_score': score,
                'prob': round(raw_prob, 2),
                'mystic_adjustment': round(mystic.get('total_mystic', 0) * 100, 2),
                'adjusted_prob': round(adj, 1),
            })
        # Normalize
        total_adj = sum(r['adjusted_prob'] for r in results)
        for r in results:
            r['adjusted_prob'] = round(r['adjusted_prob'] / total_adj * 100, 1) if total_adj > 0 else 0
        results.sort(key=lambda x: x['adjusted_prob'], reverse=True)
        r32_teams = _get_r32_teams()
        if r32_teams:
            results = [r for r in results if r['team'] in r32_teams]
        return results
    
    def get_mystic_analysis(self, team=None):
        if team:
            return compute_team_mystic(team) if 'compute_team_mystic' in globals() else {}
        return self._mystic_summary
    
    def get_mystic_summary(self):
        return self._mystic_summary
    
    def predict_match(self, team1, team2):
        return predict_h2h(team1, team2)
    
    def get_squad(self, team):
        teams_data = PLAYERS_DATA.get('teams', {})
        result = teams_data.get(team, {'team': team, 'players': [], 'error': 'No data'})
        # Add Chinese player names if available
        try:
            cn_names = CN_PLAYERS.get(team, [])
        except:
            cn_names = []
        if isinstance(result, dict) and 'players' in result:
            for i, p in enumerate(result['players']):
                if i < len(cn_names):
                    p['name_cn'] = cn_names[i]
        return result
    
    def get_elo_data(self):
        return self._elo_data
    
    def get_ucl_signals(self):
        return self._ucl_signals
    
    def monte_carlo(self, sims=5000):
        return monte_carlo_simulation(sims)
