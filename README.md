# DevConnect 🤝
### Connect. Innovate. Collaborate.

> A structured platform for students and developers to transform project ideas into working teams — replacing chaotic WhatsApp groups with a permission-based collaboration system.

🌐 **Live Demo:** https://devconnect-1-bvwy.onrender.com

---

## 📸 Preview

![DevConnect Home](https://devconnect-1-bvwy.onrender.com)

---

## 🚀 Features

- 🔐 **Secure Authentication** — Register/login with hashed passwords (Werkzeug)
- 💡 **Post Project Ideas** — Share title, description, and required skills
- 🔍 **Project Feed** — Browse all posted ideas from the community
- 📩 **Join Request System** — Send, accept, or decline collaboration requests
- 🧑‍🤝‍🧑 **Live Team View** — See active team members on every project card
- 📋 **My Requests Panel** — Track status of your sent requests (Pending / Accepted / Declined)
- 🗑️ **Delete Project** — Project owners can remove their own listings
- 📱 **Mobile Responsive** — Works on all screen sizes

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Jinja2 |
| Backend | Python 3, Flask |
| Database | SQLite + SQLAlchemy ORM |
| Auth | Werkzeug Password Hashing |
| Deployment | Render |

---

## 🏗️ Architecture

```
Three-Tier Architecture
├── Presentation Layer   → HTML5 · CSS3 · Jinja2
├── Business Logic Layer → Python · Flask Routes · Session Management
└── Data Access Layer    → SQLite · SQLAlchemy ORM
```

---

## ⚙️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/TejoRamReddy/DevConnect.git
cd DevConnect

# 2. Install dependencies
pip install flask flask-sqlalchemy werkzeug

# 3. Run the app
python app.py

# 4. Open in browser
http://localhost:5000
```

---

## 📁 Project Structure

```
DevConnect/
├── app.py                  # Flask routes and models
├── static/
│   └── style.css           # Global stylesheet
├── templates/
│   ├── home.html           # Landing page
│   ├── dashboard.html      # Main dashboard
│   ├── login.html          # Login page
│   ├── register.html       # Register page
│   └── messages.html       # Generic message page
├── requirements.txt
├── render.yaml
└── README.md
```

---

## 🔭 Roadmap

- [ ] 💬 Real-time chat (Socket.IO)
- [ ] 🤖 AI-based skill matching
- [ ] 🐙 GitHub repo integration
- [ ] 📱 Progressive Web App (PWA)
- [ ] ☁️ Scale to AWS / GCP

---

## 👨‍💻 Developer

**K. Tejo Ram**  
Department of Computer Science & Engineering  
Batch 2023 – 2027

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://linkedin.com/in/tejo-ram-reddy-3b61a130a)
[![GitHub](https://img.shields.io/badge/GitHub-TejoRamReddy-black?style=flat&logo=github)](https://github.com/TejoRamReddy)

---

## 📄 License

This project is licensed under the MIT License.