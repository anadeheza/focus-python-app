from flask import Flask, render_template, request, jsonify
import os
import jwt
import requests as req_lib
from openai import OpenAI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime


app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL', '')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")
CLERK_JWKS_URL = "https://api.clerk.com/v1/jwks"

# Cache simple para las JWKS (evita pedir las claves en cada request)
_jwks_cache = None

def get_clerk_public_keys():
    global _jwks_cache
    if _jwks_cache:
        return _jwks_cache
    try:
        resp = req_lib.get(
            CLERK_JWKS_URL,
            headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},
            timeout=5
        )
        keys = {}
        for key_data in resp.json().get("keys", []):
            kid = key_data["kid"]
            keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(key_data)
        _jwks_cache = keys
        return keys
    except Exception as e:
        print("Error fetching Clerk JWKS:", e)
        return {}

def get_clerk_user_id():
    """Verifica el JWT de Clerk del header Authorization y retorna el user_id."""
    token = request.headers.get('Authorization', '').replace('Bearer ', '').strip()
    if not token:
        return None
    try:
        public_keys = get_clerk_public_keys()
        header = jwt.get_unverified_header(token)
        key = public_keys.get(header.get("kid"))
        if not key:
            # Si no está en cache, limpiar cache y reintentar una vez
            global _jwks_cache
            _jwks_cache = None
            public_keys = get_clerk_public_keys()
            key = public_keys.get(header.get("kid"))
        if not key:
            return None
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            options={"verify_aud": False}
        )
        return payload.get("sub")
    except Exception as e:
        print("Clerk token verification error:", e)
        return None


# --------------- MODELOS ---------------

class FocusSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clerk_user_id = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, default=25)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clerk_user_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clerk_user_id = db.Column(db.String(100), unique=True, nullable=False)
    focus_duration = db.Column(db.Integer, default=25)
    break_duration = db.Column(db.Integer, default=5)
    theme = db.Column(db.String(50), default='chimney.mp4')
    volume_rain = db.Column(db.Float, default=0.0)
    volume_cafe = db.Column(db.Float, default=0.0)
    lofi_enabled = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()


# --------------- RUTAS API ---------------

@app.route('/api/sessions', methods=['POST'])
def save_session():
    user_id = get_clerk_user_id()
    if not user_id:
        return jsonify({'error': 'No autorizado'}), 401
    session = FocusSession(clerk_user_id=user_id)
    db.session.add(session)
    db.session.commit()
    return jsonify({'message': 'Sesión guardada'})

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    user_id = get_clerk_user_id()
    if not user_id:
        return jsonify({'error': 'No autorizado'}), 401
    sessions = FocusSession.query.filter_by(clerk_user_id=user_id).all()
    return jsonify([{
        'id': s.id,
        'duration': s.duration_minutes,
        'completed_at': s.completed_at.isoformat()
    } for s in sessions])

@app.route('/api/tasks', methods=['GET', 'POST'])
def tasks():
    user_id = get_clerk_user_id()
    if not user_id:
        return jsonify({'error': 'No autorizado'}), 401
    if request.method == 'POST':
        data = request.json
        task = Task(clerk_user_id=user_id, title=data['title'])
        db.session.add(task)
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})
    user_tasks = Task.query.filter_by(clerk_user_id=user_id).order_by(Task.created_at).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'completed': t.completed
    } for t in user_tasks])

@app.route('/api/tasks/<int:task_id>', methods=['PATCH', 'DELETE'])
def task_detail(task_id):
    user_id = get_clerk_user_id()
    if not user_id:
        return jsonify({'error': 'No autorizado'}), 401
    task = Task.query.filter_by(id=task_id, clerk_user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Not found'}), 404
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Deleted'})
    if request.method == 'PATCH':
        data = request.json
        if 'completed' in data:
            task.completed = data['completed']
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})

@app.route('/api/preferences', methods=['GET', 'POST'])
def preferences():
    user_id = get_clerk_user_id()
    if not user_id:
        return jsonify({'error': 'No autorizado'}), 401
    settings = UserSettings.query.filter_by(clerk_user_id=user_id).first()
    if request.method == 'POST':
        data = request.json
        if not settings:
            settings = UserSettings(clerk_user_id=user_id)
            db.session.add(settings)
        if 'theme' in data:
            settings.theme = data['theme']
        if 'volume_rain' in data:
            settings.volume_rain = data['volume_rain']
        if 'volume_cafe' in data:
            settings.volume_cafe = data['volume_cafe']
        if 'lofi_enabled' in data:
            settings.lofi_enabled = data['lofi_enabled']
        db.session.commit()
        return jsonify({'message': 'Saved'})
    # GET
    if not settings:
        return jsonify({'theme': 'chimney.mp4', 'volume_rain': 0.0, 'volume_cafe': 0.0, 'lofi_enabled': False})
    return jsonify({
        'theme': settings.theme,
        'volume_rain': settings.volume_rain,
        'volume_cafe': settings.volume_cafe,
        'lofi_enabled': settings.lofi_enabled
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is empty'}), 400

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": "You are a helpful, concise AI study and work assistant inside a focus timer app. Give actionable, clear, and encouraging advice for studying, coding, or managing tasks."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'reply': response.choices[0].message.content})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({'error': 'Could not connect to AI server.'}), 500

@app.route('/api/summary', methods=['POST'])
def summary():
    try:
        data = request.json
        completed_tasks = data.get('tasks', [])
        
        if completed_tasks:
            tasks_str = ", ".join(completed_tasks)
            prompt = f"The user just finished a 25-minute focus session and successfully completed these tasks: {tasks_str}. Write a short, calm congratulatory message addressing these specific achievements."
        else:
            prompt = "The user just finished a 25-minute focus session, but didn't check off any tasks. Write a short, encouraging message congratulating them on completing the focus block itself and boosting their stamina."

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {
                    "role": "system",
                    "content": "You are a study partner. Give a calm, simple congratulations message. Mention the completed achievements explicitly if provided. Keep it brief and under 30 words total."
                },
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({'summary': response.choices[0].message.content})
    except Exception as e:
        print("Summary error:", e)
        return jsonify({'summary': "Exceptional focus out there! Take a well-deserved break ☕︎"})

if __name__ == '__main__':
    app.run(debug=True)