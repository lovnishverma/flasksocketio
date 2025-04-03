# Flask Chat App with Nicknames

A real-time chat application built with Flask, Flask-SocketIO, and MongoDB. Users can join the chat, set their nickname, and send messages with timestamps in IST.

## Features
- **Real-time messaging** using WebSockets (Flask-SocketIO)
- **Persistent chat history** stored in MongoDB
- **User nicknames** instead of anonymous messages
- **Dark/Light theme toggle** for better user experience
- **Responsive UI** with Bootstrap

## Tech Stack
- **Backend:** Flask, Flask-SocketIO, PyMongo, Gevent
- **Frontend:** HTML, CSS, Bootstrap, JavaScript (jQuery, Socket.io)
- **Database:** MongoDB Atlas

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/lovnishverma/flasksocketio.git
cd flasksocketio
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB
Update `MONGO_URI` in `app.py` with your MongoDB connection string.

### 5. Run the App
```bash
python app.py
```

The app will run on `http://127.0.0.1:5000/`

## Usage
1. Open the app in your browser.
2. Enter a nickname in the input field.
3. Type messages and send them.
4. Messages are stored in MongoDB with timestamps in IST.

## Project Structure
```
flask-chat-app/
│-- static/
│-- templates/
│   ├── index.html
│-- app.py
│-- requirements.txt
│-- README.md
```

## Dependencies
```
flask
flask-socketio
pymongo
gevent
gevent-monkey
pytz
```

## Contributing
Feel free to fork and submit pull requests. Contributions are welcome!

## License
MIT License
