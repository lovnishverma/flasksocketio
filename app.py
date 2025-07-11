from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from datetime import datetime
import pytz
import gevent
import gevent.monkey

# Apply gevent monkey patching before importing other modules
gevent.monkey.patch_all()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lovnish_super_secret_key'
socketio = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://test:test@cluster0.sxci1.mongodb.net/chatDB?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client['lovnishdarkchatDB']
messages_collection = db['messages']

# Define timezone
IST = pytz.timezone('Asia/Kolkata')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Send past messages when a user connects."""
    try:
        # Sort messages by timestamp to get them in chronological order
        past_messages = list(messages_collection.find({}).sort('timestamp', 1))
        
        for msg in past_messages:
            msg['_id'] = str(msg['_id'])  # Convert ObjectId to string
            
            if 'timestamp' in msg:
                try:
                    # Handle different timestamp formats
                    if isinstance(msg['timestamp'], str):
                        msg['timestamp'] = datetime.strptime(msg['timestamp'], '%Y-%m-%d %H:%M:%S')
                    
                    # Ensure timezone awareness
                    if msg['timestamp'].tzinfo is None:
                        msg['timestamp'] = pytz.utc.localize(msg['timestamp'])
                    
                    # Convert to IST and format
                    ist_time = msg['timestamp'].astimezone(IST)
                    msg['timestamp'] = ist_time.strftime("%d-%m-%Y %I:%M %p")
                    
                except Exception as e:
                    print(f"Error parsing timestamp: {e}")
                    msg['timestamp'] = "Unknown"
            else:
                msg['timestamp'] = "Unknown"
        
        emit('load_messages', past_messages)
        print(f"Loaded {len(past_messages)} past messages for new user")
        
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        emit('load_messages', [])

@socketio.on('message')
def handle_message(data):
    """Store messages with nickname in MongoDB and broadcast."""
    try:
        nickname = data.get('nickname', 'Anonymous')
        message_text = data.get('message', '')
        
        # Validate input
        if not message_text.strip():
            return
        
        # Create timestamp
        utc_now = datetime.utcnow()
        utc_now = pytz.utc.localize(utc_now)
        ist_now = utc_now.astimezone(IST)
        
        # Create message document
        message_doc = {
            'nickname': nickname,
            'message': message_text.strip(),
            'timestamp': utc_now  # Store in UTC
        }
        
        # Insert into database
        inserted_doc = messages_collection.insert_one(message_doc)
        
        # Prepare message for broadcasting
        message_doc['_id'] = str(inserted_doc.inserted_id)
        message_doc['timestamp'] = ist_now.strftime("%d-%m-%Y %I:%M %p")
        
        # Broadcast to all connected clients
        emit('message', message_doc, broadcast=True)
        print(f"Message from {nickname}: {message_text[:50]}...")
        
    except Exception as e:
        print(f"Error handling message: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection."""
    print('User disconnected')

@socketio.on('connect_error')
def handle_connect_error(error):
    """Handle connection errors."""
    print(f"Connection error: {error}")

if __name__ == '__main__':
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Run the application
        socketio.run(app, host="0.0.0.0", port=5000, debug=True)
        
    except Exception as e:
        print(f"Failed to start application: {e}")
    finally:
        client.close()
