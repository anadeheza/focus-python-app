from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

client = OpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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
            model="gemini-2.0-flash", 
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
        return jsonify({'summary': "Exceptional focus out there! Take a well-deserved break ☕︎"})

if __name__ == '__main__':
    app.run(debug=True)