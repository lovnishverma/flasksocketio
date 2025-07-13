# 🗨️ Flask Chat App with Nicknames

A real-time anonymous chat app built using **Flask**, **Flask-SocketIO**, and **MongoDB**, featuring user nicknames, timestamped messages, and a responsive UI with light/dark themes.

> 🔥 Live Demo: [https://flasksocketio.onrender.com](https://flasksocketio.onrender.com)

---

## ✨ Features

* 💬 Real-time chat with **WebSockets (Socket.IO)**
* 🧠 User **nicknames** (saved in browser)
* 🕒 Message **timestamps in IST**
* 🗃️ **Persistent chat history** (MongoDB)
* 🎨 Toggle between **light/dark theme**
* 📱 **Mobile-friendly** UI with Bootstrap 5

---

## 🛠️ Tech Stack

| Layer      | Technology                                    |
| ---------- | --------------------------------------------- |
| Backend    | Flask, Flask-SocketIO, Gevent, PyMongo        |
| Frontend   | HTML, CSS, Bootstrap 5, JavaScript, Socket.IO |
| Database   | MongoDB Atlas                                 |
| Deployment | Docker, Render.com                            |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/lovnishverma/flasksocketio.git
cd flasksocketio
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB

Edit the `MONGO_URI` in `app.py`:

```python
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/chatDB?retryWrites=true&w=majority"
```

You can get this URI from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

### 5. Run the App Locally

```bash
python app.py
```

App runs at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🐳 Docker Support

### Build the Docker Image

```bash
docker build -t flask-chat-app .
```

### Run the Container

```bash
docker run -p 10000:10000 flask-chat-app
```

Open [http://localhost:10000](http://localhost:10000)

---

## 📁 Project Structure

```
flasksocketio/
│
├── app.py                  # Main Flask app
├── requirements.txt        # Python dependencies
├── Dockerfile              # For containerization
├── templates/
│   └── index.html          # Chat interface
└── static/                 # (Optional) static files
```

---

## 📦 requirements.txt

```txt
certifi==2021.10.8
click==7.1.2
dnspython==1.16.0
eventlet==0.21.0
Flask==0.12.4
Flask-PyMongo==2.3.0
Flask-SocketIO==2.9.6
gevent==1.3.7
gevent-websocket==0.10.1
greenlet==0.4.15
Jinja2==2.11.3
MarkupSafe==1.1.1
pymongo==3.7.2
python-engineio==3.13.2
python-socketio==4.5.1
pytz==2021.1
requests==2.27.1
six==1.16.0
urllib3==1.26.20
Werkzeug==1.0.1
gunicorn
```

---

## 🌐 Deploying on [Render](https://render.com/)

1. Connect GitHub repo to Render.
2. Use the following settings:

   * **Environment**: Docker
   * **Port**: Auto-detect (expose 10000)
   * **Build Command**: *(Leave blank)*
   * **Start Command**: *(Handled by `CMD` in Dockerfile)*

✅ Render will detect the port and start your Flask-SocketIO app with `gunicorn`.

---


## 📸 Screenshots

| Dark Theme                                         | Light Theme                                         |
| -------------------------------------------------- | --------------------------------------------------- |
| ![Dark Theme](https://github.com/user-attachments/assets/8b969b0f-eb81-4b0c-9524-490a4100267f) | ![Light Theme](https://github.com/user-attachments/assets/24012702-6a0c-436e-9558-394c280efb93) |

---

## 🤝 Contributing

Feel free to fork, improve, and submit PRs!

---

## 📄 License

MIT License – [Lovnish Verma](https://github.com/lovnishverma)

---
