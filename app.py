from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from pymongo import MongoClient
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Explicitly set async_mode to 'gevent'
socketio = SocketIO(app, async_mode='gevent')

# MongoDB Atlas URI
MONGO_URI = os.environ.get('MONGO_URI')  # will set from Render Dashboard
client = MongoClient(MONGO_URI)
db = client['chat_db']
messages = db['messages']

# IST Timezone
tz = pytz.timezone('Asia/Kolkata')

@app.route('/')
def index():
    all_messages = list(messages.find({}, {'_id': 0}))
    return render_template('index.html', messages=all_messages)

@socketio.on('message')
def handle_message(msg):
    nickname = msg['nickname']
    message_text = msg['message']
    timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
    
    chat_message = {
        'nickname': nickname,
        'message': message_text,
        'timestamp': timestamp
    }
    
    # Insert into DB
    result = messages.insert_one(chat_message)

    # Remove `_id` field added by MongoDB before broadcasting
    chat_message.pop('_id', None)

    # Broadcast to all clients
    send(chat_message, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
