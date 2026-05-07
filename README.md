# ContentForgeAI 🚀
AI-Powered Content Creation Platform built using Flask, PostgreSQL, OpenAI, ElevenLabs, FFmpeg, and modern AI workflows.

ContentForgeAI helps creators generate AI-powered blogs, captions, scripts, and short-form reels/videos through an integrated web platform.

## ✨ Features

### 🧠 AI Content Generation
- AI Reel Generator
- AI Blog Generator
- AI Caption Generator
- AI Script Generator
- AI Content Assistance
- Smart Prompt-Based Content Creation

### 🎬 AI Reel Generator
- Upload media assets
- Generate AI-powered short reels
- FFmpeg-based video processing
- Duration-based scene generation
- Automated media stitching

### 🔐 Authentication System
- User Signup/Login
- Session-based authentication
- Password hashing & security
- Persistent user history

### 📜 History Management
- Generated content history
- Reel generation history
- Polling-based processing updates
- Status tracking

### ☁️ Cloud Deployment
- Render deployment
- Neon PostgreSQL database
- Environment variable configuration
- Production-ready backend setup

---

# 🛠️ Tech Stack

## Backend
- Flask
- Flask-SQLAlchemy
- Jinja2
- Gunicorn

## Frontend
- HTML
- Tailwind CSS
- JavaScript

## Database
- PostgreSQL
- Neon Database

## AI Services
- OpenAI API
- ElevenLabs API

## Video Processing
- FFmpeg

## Version Control
- Git
- GitHub

## Deployment
- Render

---

# 📂 Project Structure

```bash
ContentForgeAI/
│
├── static/
│   ├── css/
│   ├── js/
│
├── templates/
│
├── models.py
├── app.py
├── requirements.txt
│
├── blogGenerator.py
├── reelGenerator.py
├── captionGenerator.py
│
└── user_uploads_reelGen/
```

---

# ⚙️ Environment Variables

Create a `.env` file in the root directory.

```env
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
SECRET_KEY=your_secret_key
DATABASE_URL=your_postgresql_uri
```

---

# 🚀 Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/SubratKumarSingh2001/ContentForgeAI-AI-Powered-Content-Creation.git
cd ContentForgeAI-AI-Powered-Content-Creation
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Install FFmpeg

Download and install FFmpeg:

- Windows: https://ffmpeg.org/download.html
- Add FFmpeg to system PATH

Verify installation:

```bash
ffmpeg -version
```

---

## 5️⃣ Run Application

```bash
python app.py
```

or

```bash
flask run
```

---

# 🌐 Deployment

## Render Deployment

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn wsgi:app #wsgi(replace it with you flask app name)
```

---

# 🗄️ Database

The project uses PostgreSQL with Neon cloud database.

SQLAlchemy models automatically create tables using:

```python
with app.app_context():
    db.create_all()
```

---

# 🔐 Authentication

Passwords are securely stored using hashing methods.

User sessions are managed using Flask session handling.

---

# 🎥 Reel Generation Workflow

1. User uploads media files
2. Files stored temporarily
3. AI generates content/script
4. FFmpeg processes video
5. Final reel generated
6. Status updated in database

---

# 🧩 Architecture Overview

```text
                    ┌────────────────────┐
                    │     Frontend       │
                    │ HTML • CSS • JS    │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   Flask Backend    │
                    │  Routes & Logic    │
                    └─────────┬──────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼

 ┌───────────────┐   ┌────────────────┐   ┌────────────────┐
 │ OpenAI API    │   │ ElevenLabs API │   │ FFmpeg Engine  │
 │ AI Generation │   │ Voice/TTS      │   │ Video Creation │
 └───────────────┘   └────────────────┘   └────────────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │ Neon PostgreSQL DB │
                    │ User & History Data│
                    └────────────────────┘
```

---

# 📌 Future Improvements

- Background job queues
- Cloud storage integration
- AI thumbnail generation
- Multi-language support
- Advanced reel templates
- OAuth authentication

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Subrat Kumar Singh

GitHub:
https://github.com/SubratKumarSingh2001