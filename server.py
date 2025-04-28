from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Đường dẫn đến file chat.txt
CHAT_FILE = 'chat.txt'

# Hàm để đọc tin nhắn từ file chat.txt
def read_messages():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, 'r', encoding='utf-8') as file:
            messages = file.readlines()
        return [msg.strip() for msg in messages]
    return []

# Hàm để ghi tin nhắn vào file chat.txt
def write_message(message):
    with open(CHAT_FILE, 'a', encoding='utf-8') as file:
        file.write(message + '\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_messages', methods=['GET'])
def get_messages():
    messages = read_messages()
    formatted_messages = []
    for message in messages:
        if ':' in message:
            name, text = message.split(":", 1)
            formatted_messages.append({'name': name.strip(), 'text': text.strip()})
        else:
            # Nếu dòng không có dấu ':', gán name là "Hệ thống"
            formatted_messages.append({'name': 'Hệ thống', 'text': message.strip()})
    return jsonify({'messages': formatted_messages})

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    name = request.form.get('name')
    if message and name:
        formatted_message = f"{name}: {message}"
        write_message(formatted_message)
    return '', 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Quan trọng nếu deploy Render
    app.run(debug=True, host='0.0.0.0', port=port)
