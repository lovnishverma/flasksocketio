from flask import Flask, render_template, request
from flask_socketio import SocketIO, send
from pymongo import MongoClient
from datetime import datetime
import pytz
import os
import eventlet

# ✅ Monkey patching for eventlet
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# ✅ Initialize SocketIO with eventlet
socketio = SocketIO(app, async_mode='eventlet')

# ✅ MongoDB Atlas URI from environment
MONGO_URI = os.environ.get('MONGO_URI')  # Set this in Render Dashboard
client = MongoClient(MONGO_URI)
db = client['chat_db']
messages = db['messages']

# ✅ IST Timezone
tz = pytz.timezone('Asia/Kolkata')

@app.route('/')
def index():
    all_messages = list(messages.find({}, {'_id': 0}))
    return render_template('index.html', messages=all_messages)

@socketio.on('message')
def handle_message(msg):
    nickname = msg.get('nickname')
    message_text = msg.get('message')
    timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    chat_message = {
        'nickname': nickname,
        'message': message_text,
        'timestamp': timestamp
    }

    # ✅ Insert into MongoDB
    messages.insert_one(chat_message)

    # ✅ Remove MongoDB's _id field before sending
    chat_message.pop('_id', None)

    # ✅ Broadcast to all connected clients
    send(chat_message, broadcast=True)

if __name__ == '__main__':
    # ✅ Use eventlet WSGI server (REQUIRED for WebSocket support)
    socketio.run(app, host='0.0.0.0', port=5000)
