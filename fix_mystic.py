import re

with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the compute_team_mystic function and replace it entirely
start = content.find('def compute_team_mystic(')
end = content.find('\ndef compute_all_mystic():')
if start > 0 and end > start:
    new_func = '''def compute_team_mystic(team_name):
    try:
        elo = get_elo(team_name) or 1700
        mf = compute_mystic_factor(team_name, elo)
        hosts = ['United States', 'Canada', 'Mexico']
        is_host = team_name in hosts
        is_defending = team_name == 'Argentina'
        score = compute_team_score(team_name)
        if not isinstance(score, dict):
            score = {'total_score': 0.5, 'avg_age': None}
        logical_prob = score.get('total_score', 0.5)
        avg_age = score.get('avg_age', None)
        if logical_prob > 0.8: stage1 = cn(team_name) + "是本届夺冠热门"
        elif logical_prob > 0.6: stage1 = cn(team_name) + "具备八强以上实力"
        else: stage1 = cn(team_name) + "属于中游球队"
        biases = []
        if mf.get('favorite_curse', 0) < -0.01: biases.append("强势方诅咒")
        if mf.get('host_bonus', 0) > 0: biases.append("东道主优势")
        stage2 = "、".join(biases) if biases else "数据清晰无偏差"
        if is_defending: stage3 = "卫冕冠军背负历史重担"
        elif is_host: stage3 = "东道主占据天时地利"
        elif avg_age and avg_age < 26: stage3 = "青春风暴"
        else: stage3 = "成熟稳健"
        if elo > 1850: tao = "反者道之动——盛极而衰"
        elif elo < 1650: tao = "柔弱胜刚强——无包袱爆发"
        else: tao = "道法自然——顺势而为"
        if is_host: gua = "泰卦——东道主天时地利"
        elif is_defending: gua = "否卦——卫冕压力内耗"
        elif elo > 1880: gua = "乾卦——亢龙有悔"
        elif elo < 1650: gua = "坤卦——以柔克刚"
        elif avg_age and avg_age < 26: gua = "震卦——雷动活力"
        else: gua = "观卦——观仰伺机"
        return {'team': team_name, 'team_cn': cn(team_name), 'elo': elo,
                'three_stages': {'stage1': stage1, 'stage2': stage2, 'stage3': stage3},
                'tao_te_ching': tao, 'i_ching': gua, 'mystic_factors': mf}
    except Exception as e:
        return {'team': team_name, 'team_cn': cn(team_name), 'error': str(e)}
'''
    content = content[:start] + new_func + content[end:]
    with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Function replaced successfully')
else:
    print(f'Could not find function boundaries: start={start}, end={end}')
