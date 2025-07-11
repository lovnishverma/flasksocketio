# ✅ Apply eventlet monkey patching
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lovnish_super_secret_key'
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# MongoDB connection
MONGO_URI = "mongodb+srv://test:test@cluster0.sxci1.mongodb.net/chatDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['lovnishdarkchatDB']
messages_collection = db['messages']
IST = pytz.timezone('Asia/Kolkata')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    try:
        past_messages = list(messages_collection.find({}).sort('timestamp', 1))
        for msg in past_messages:
            msg['_id'] = str(msg['_id'])
            if 'timestamp' in msg:
                try:
                    if isinstance(msg['timestamp'], str):
                        msg['timestamp'] = datetime.strptime(msg['timestamp'], '%Y-%m-%d %H:%M:%S')
                    if msg['timestamp'].tzinfo is None:
                        msg['timestamp'] = pytz.utc.localize(msg['timestamp'])
                    ist_time = msg['timestamp'].astimezone(IST)
                    msg['timestamp'] = ist_time.strftime("%d-%m-%Y %I:%M %p")
                except Exception as e:
                    print(f"Timestamp parse error: {e}")
                    msg['timestamp'] = "Unknown"
            else:
                msg['timestamp'] = "Unknown"
        emit('load_messages', past_messages)
    except Exception as e:
        print(f"Mongo error: {e}")
        emit('load_messages', [])

@socketio.on('message')
def handle_message(data):
    try:
        nickname = data.get('nickname', 'Anonymous')
        message_text = data.get('message', '').strip()
        if not message_text:
            return
        utc_now = datetime.utcnow()
        utc_now = pytz.utc.localize(utc_now)
        ist_now = utc_now.astimezone(IST)
        doc = {
            'nickname': nickname,
            'message': message_text,
            'timestamp': utc_now
        }
        inserted = messages_collection.insert_one(doc)
        doc['_id'] = str(inserted.inserted_id)
        doc['timestamp'] = ist_now.strftime("%d-%m-%Y %I:%M %p")
        emit('message', doc, broadcast=True)
    except Exception as e:
        print(f"Error handling message: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    print("User disconnected")

@socketio.on('connect_error')
def handle_connect_error(error):
    print(f"Connection error: {error}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
