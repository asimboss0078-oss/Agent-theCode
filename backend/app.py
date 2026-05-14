import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from supabase_manager import SupabaseManager
from api_key_manager import APIKeyManager
from web_fetcher import fetch_web_content, parse_web_answer

app = Flask(__name__)
CORS(app)

# Multi-account Supabase support
supabase_manager = SupabaseManager(os.getenv('SUPABASE_CREDENTIALS'))

# Multi-token external APIs (e.g., por-api)
api_key_manager = APIKeyManager(os.getenv('POR_API_TOKENS'))

@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get('message', '')
    # 1. Check custom Supabase memory first
    context, used_supabase = supabase_manager.get_context_for_query(user_msg)
    # 2. Attempt web fetch if query triggers web need
    web_answer = ''
    if should_fetch_web(user_msg, context):
        url = extract_web_url(user_msg)
        if url:
            page_content = fetch_web_content(url)
            web_answer = parse_web_answer(page_content)
    # 3. Get response from AI Model (with context, web_answer, user_msg)
    ai_response = run_local_model(user_msg, context, web_answer)
    return jsonify({
        "answer": ai_response,
        "web_content": web_answer,
        "context_used": context,
        "supabase_used": used_supabase
    })

@app.route('/api/train', methods=['POST'])
def train():
    txt = request.form.get('text') or (request.files['file'].read().decode() if 'file' in request.files else '')
    label = request.form.get('label', 'default')
    supabase_manager.add_training_text(label, txt)
    return jsonify({"status": "ok", "added": len(txt)})

@app.route('/api/web_preview', methods=['POST'])
def web_preview():
    url = request.json.get('url')
    raw_html = fetch_web_content(url)
    preview = parse_web_answer(raw_html, html_render=True)
    return jsonify({"preview": preview})

@app.route('/api/supabase_accounts', methods=['GET', 'POST'])
def supabase_accounts():
    if request.method == 'POST':
        creds = request.json
        supabase_manager.add_account(creds)
        return jsonify({'ok': True})
    else:
        return jsonify(supabase_manager.list_accounts())

@app.route('/api/api_keys', methods=['GET', 'POST'])
def api_keys():
    if request.method == 'POST':
        key = request.json.get('key')
        api_key_manager.add_key(key)
        return jsonify({'ok': True})
    else:
        return jsonify(api_key_manager.list_keys())

# Serve static training data for preview (optional)
@app.route('/training_data/<label>/<filename>')
def get_training_data(label, filename):
    return send_from_directory(f'../training_data/{label}', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
