with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'r', encoding='utf-8') as f:
    e = f.read()

# Simpler, more differentiated goal prediction based on Elo gap
old = """    avg = 0.65
    strength_a = score_val_a / avg
    strength_b = score_val_b / avg
    lambda_a = 0.2 + 1.0 * strength_a + elo_diff / 3000.0
    lambda_b = 0.2 + 1.0 * strength_b - elo_diff / 3000.0"""

new = """    lambda_a = 0.6 + 1.1 * (score_val_a / 0.65) + elo_diff / 1500.0
    lambda_b = 0.6 + 1.1 * (score_val_b / 0.65) - elo_diff / 1500.0"""

e = e.replace(old, new)

# Also update noise range to be slightly wider for differentiation
old_noise = """    # Score prediction: small consistent noise for natural variety
    rng = random.Random(hash(team_a + team_b) % 100000)
    noise_a = rng.uniform(-0.15, 0.15)
    noise_b = rng.uniform(-0.15, 0.15)"""

new_noise = """    # Score prediction: consistent noise for variety
    rng = random.Random(hash(team_a + team_b) % 100000)
    noise_a = rng.uniform(-0.2, 0.2)
    noise_b = rng.uniform(-0.2, 0.2)"""

e = e.replace(old_noise, new_noise)

with open('E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'w', encoding='utf-8') as f:
    f.write(e)

import subprocess
subprocess.run(['scp', '-i', r'E:\Workspace\claude\115.190.112.212 SSH Secret.pem', '-o', 'StrictHostKeyChecking=no',
    'E:/Workspace/Kun/WCUP2026/prediction/engine.py', 'root@115.190.112.212:/root/wcup2026/prediction/engine.py'])

# Kill old process
subprocess.run(['ssh', '-i', r'E:\Workspace\claude\115.190.112.212 SSH Secret.pem', '-o', 'StrictHostKeyChecking=no',
    'root@115.190.112.212', 'kill -9 $(fuser 10088/tcp 2>/dev/null); sleep 2; cd /root/wcup2026 && nohup venv/bin/python app.py > /var/log/wcup2026.log 2>&1 &'])
print('Done')
