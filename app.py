from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from datetime import datetime
import pytz
import os

# Setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Setup SocketIO
socketio = SocketIO(app)

# Setup MongoDB
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://<username>:<password>@cluster0.mongodb.net/chatdb?retryWrites=true&w=majority')
client = MongoClient(MONGO_URI)
db = client.get_database("chatdb")
messages_collection = db.get_collection("messages")

# Timezone for IST
IST = pytz.timezone('Asia/Kolkata')

@app.route('/')
def index():
    # Fetch messages from MongoDB
    messages = list(messages_collection.find({}, {"_id": 0}))
    return render_template('index.html', messages=messages)

@socketio.on('send_message')
def handle_send_message(data):
    nickname = data.get('nickname')
    message = data.get('message')
    timestamp = datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')
    
    full_message = {
        "nickname": nickname,
        "message": message,
        "timestamp": timestamp
    }

    # Save to MongoDB
    messages_collection.insert_one(full_message)
    
    # Broadcast to all clients
    emit('receive_message', full_message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
