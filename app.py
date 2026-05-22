from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

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
            model="llama3",  
            messages=[
                {"role": "system", "content": "You are a helpful, concise AI study and work assistant inside a focus timer app. Give actionable, clear, and encouraging advice for studying, coding, or managing tasks."},
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'reply': response.choices[0].message.content})
    except Exception as e:
        return jsonify({'error': 'Could not connect to local AI server.'}), 500
    

@app.route('/api/summary', methods=['POST'])
def summary():
    try:
        data = request.json
        current_tasks = data.get('tasks', [])
        
        tasks_str = ", ".join(current_tasks) if current_tasks else "focusing deeply"
        prompt = f"The user just completed a productive 25-minute focus session. Their active tasks were: {tasks_str}. Write a very short, 2-sentence celebratory, retro-arcade-style victory message praising their focus and encouraging a short break."

        response = client.chat.completions.create(
            model="llama3",  
            messages=[
                {"role": "system", "content": "You are a retro-arcade game announcer system. Speak in an encouraging, punchy, classic 8-bit or pixel-arcade style syntax. Keep it under 50 words total."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({'summary': response.choices[0].message.content})
    except Exception as e:
        return jsonify({'summary': "🏆 Session complete! Great work out there explorer. Take a well-deserved break!"})

if __name__ == '__main__':
    app.run(debug=True)