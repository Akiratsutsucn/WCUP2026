import json
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ─── Static ───────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# ─── API ──────────────────────────────────────────────────
@app.route('/api/teams')
def api_teams():
    return jsonify(load_json('teams.json'))

@app.route('/api/standings')
def api_standings():
    data = load_json('standings.json')
    if data:
        return jsonify(data)
    return jsonify({"error": "No standings data"}), 404

@app.route('/api/all')
def api_all():
    """Return all data in one call."""
    return jsonify({
        'teams': load_json('teams.json'),
        'matches': load_json('matches.json'),
        'standings': load_json('standings.json')
    })

@app.route('/api/matches')
def api_matches():
    data = load_json('matches.json')
    if data:
        return jsonify(data)
    return jsonify({"error": "No match data"}), 404

@app.route('/api/match', methods=['POST'])
def update_match():
    """Update a match result. Body: {id, home_score, away_score, home_pen, away_pen}"""
    body = request.get_json()
    match_id = body.get('id')
    home_score = body.get('home_score')
    away_score = body.get('away_score')
    home_pen = body.get('home_pen')
    away_pen = body.get('away_pen')

    data = load_json('matches.json')
    if not data:
        return jsonify({"error": "No match data"}), 404

    # Find and update the match
    updated = None
    for m in data['matches']:
        if m['id'] == match_id:
            m['home_score'] = home_score
            m['away_score'] = away_score
            m['home_pen'] = home_pen
            m['away_pen'] = away_pen

            # Determine winner
            if home_score is not None and away_score is not None:
                if home_score > away_score:
                    m['winner'] = 'home'
                elif away_score > home_score:
                    m['winner'] = 'away'
                elif home_pen is not None and away_pen is not None:
                    m['winner'] = 'home' if home_pen > away_pen else 'away'
                else:
                    m['winner'] = None  # draw with no penalties yet
            else:
                m['winner'] = None

            updated = m
            break

    if not updated:
        return jsonify({"error": "Match not found"}), 404

    # Auto-advance: propagate winner to next match
    propagate_winners(data)

    save_json('matches.json', data)
    return jsonify(updated)

def propagate_winners(data):
    """For each match with a winner, populate that team into the next match."""
    matches = {m['id']: m for m in data['matches']}
    
    # Reset all home/away in rounds R16 and beyond (will be re-populated)
    for m in data['matches']:
        if m['round'] != 'R32':
            m['home'] = None
            m['away'] = None

    for m in data['matches']:
        if m['winner'] and m.get('next'):
            next_match = matches.get(m['next'])
            if next_match:
                winner_team = m['home'] if m['winner'] == 'home' else m['away']
                # Determine which slot: feeds into home if match id odd in its group
                if not next_match['home']:
                    next_match['home'] = winner_team
                elif not next_match['away']:
                    next_match['away'] = winner_team
                else:
                    # Both slots filled - keep existing
                    pass
        
        # Handle 3rd place match (losers of semifinals)
        if m['round'] == 'SF' and m['winner'] and m.get('loser_next'):
            loser_next = matches.get(m['loser_next'])
            if loser_next:
                loser_team = m['away'] if m['winner'] == 'home' else m['home']
                if not loser_next['home']:
                    loser_next['home'] = loser_team
                elif not loser_next['away']:
                    loser_next['away'] = loser_team


@app.route('/api/match/teams', methods=['POST'])
def set_match_teams():
    """Manually set teams for a match. Body: {id, home, away}"""
    body = request.get_json()
    match_id = body.get('id')

    data = load_json('matches.json')
    if not data:
        return jsonify({"error": "No match data"}), 404

    for m in data['matches']:
        if m['id'] == match_id:
            if 'home' in body:
                m['home'] = body['home']
            if 'away' in body:
                m['away'] = body['away']
            save_json('matches.json', data)
            return jsonify(m)

    return jsonify({"error": "Match not found"}), 404


@app.route('/api/reset', methods=['POST'])
def reset_matches():
    """Reset all knockout matches to initial state."""
    data = load_json('matches.json')
    if not data:
        return jsonify({"error": "No match data"}), 404

    for m in data['matches']:
        m['home_score'] = None
        m['away_score'] = None
        m['home_pen'] = None
        m['away_pen'] = None
        m['winner'] = None
        if m['round'] != 'R32':
            m['home'] = None
            m['away'] = None
        else:
            m['home'] = None
            m['away'] = None

    save_json('matches.json', data)
    return jsonify({"status": "reset"})


# ─── 预测 API ───────────────────────────────────────────
try:
    from prediction.engine import PredictionEngine
    _pred_engine = PredictionEngine()
    _pred_ready = True
except Exception as e:
    _pred_engine = None
    _pred_ready = False
    print(f"[WARN] Prediction engine not available: {e}")

@app.route('/api/predict/rankings')
def api_predict_rankings():
    """冠军预测排行"""
    if not _pred_ready:
        return jsonify({"error": "Prediction engine not available"}), 503
    data = _pred_engine.get_rankings()
    return jsonify(data)

@app.route('/api/predict/h2h')
def api_predict_h2h():
    """H2H对战预测"""
    if not _pred_ready:
        return jsonify({"error": "Prediction engine not available"}), 503
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    if not team1 or not team2:
        return jsonify({"error": "Need team1 and team2 params"}), 400
    data = _pred_engine.predict_match(team1, team2)
    return jsonify(data)

@app.route('/api/predict/mystic')
def api_predict_mystic():
    """玄学因子分析"""
    if not _pred_ready:
        return jsonify({"error": "Prediction engine not available"}), 503
    team = request.args.get('team')
    data = _pred_engine.get_mystic_analysis(team)
    return jsonify(data)

@app.route('/api/predict/squad')
def api_predict_squad():
    """球队球员阵容"""
    if not _pred_ready:
        return jsonify({"error": "Prediction engine not available"}), 503
    team = request.args.get('team')
    data = _pred_engine.get_squad(team)
    return jsonify(data)

@app.route('/api/predict/suspensions')
def api_predict_suspensions():
    """伤病和停赛信息"""
    # Will be enhanced with live data, returns static for now
    susp_data = load_json('suspensions.json') or {}
    return jsonify(susp_data)

@app.route('/api/predict/all')
def api_predict_all():
    """一次性获取所有预测数据"""
    if not _pred_ready:
        return jsonify({"error": "Prediction engine not available"}), 503
    data = {
        'rankings': _pred_engine.get_rankings(),
        'mystic_summary': _pred_engine.get_mystic_summary(),
        'suspensions': load_json('suspensions.json') or {},
        'elo_data': _pred_engine.get_elo_data(),
        'ucl_signals': _pred_engine.get_ucl_signals(),
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10088, debug=True)
