with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'r', encoding='utf-8') as f:
    h = f.read()

# Remove button
h = h.replace('<button class="btn-sm" onclick="loadMysticDetail()">查看详情</button>', '')

# Also rewrite compute_team_mystic in engine.py to be more varied
with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'r', encoding='utf-8') as f:
    e = f.read()

# Find and replace the entire function
start = e.find('def compute_team_mystic(')
end = e.find('\ndef compute_all_mystic():')
if start > 0 and end > start:
    new_func = '''def compute_team_mystic(team_name):
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
        if logical_prob > 0.85: s1 = cn(team_name)+"综合实力顶级，是本届冠军最有力争夺者之一。Elo评分"+str(round(elo))+"，阵容深度与球星个人能力兼备。"
        elif logical_prob > 0.75: s1 = cn(team_name)+"整体实力强劲，具备冲击四强的资本。Elo评分"+str(round(elo))+"，攻防体系成熟。"
        elif logical_prob > 0.65: s1 = cn(team_name)+"战力处于中上游，淘汰赛签运将很大程度决定能走多远。Elo"+str(round(elo))+"。"
        elif logical_prob > 0.55: s1 = cn(team_name)+"属于中游球队，需要在关键比赛超常发挥才能突破。Elo"+str(round(elo))+"。"
        elif logical_prob > 0.45: s1 = cn(team_name)+"实力偏弱，但世界杯历史上从不缺少黑马。Elo"+str(round(elo))+"。"
        else: s1 = cn(team_name)+"纸面实力不占优，但不被看好反而可能成为最大优势。Elo"+str(round(elo))+"。"
        
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
'''
    e = e[:start] + new_func + e[end:]
    with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'w', encoding='utf-8') as f:
        f.write(e)

with open('E:/Workspace/Kun/WCUP2026/static/index.html', 'w', encoding='utf-8') as f:
    f.write(h)
print('Both fixed')
