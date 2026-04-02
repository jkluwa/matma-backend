# 🧮⚔️ Math Arena API

A real-time, competitive backend platform for 1v1 math duels. Built with **FastAPI** and **WebSockets**, this API manages lobbies, dynamic matchmaking, and real-time task distribution. 

## 🎮 How It Works (The Game Flow)
1. **👑 Admin Initialization:** The Admin logs in and opens the arena.
2. **👤 Player Joining:** Users join the lobby simply by providing a nickname (no complex registration required).
3. **🚀 Match Initiation:** The Admin clicks "Start Game".
4. **🔀 Dynamic Matchmaking:** The server automatically pairs active users into 1v1 duels.
5. **📝 The Battle:** Each pair receives the exact same mathematical task from the database.
6. **🏆 The Finish (WIP):** Players race to solve the task first.

## 🛠 Tech Stack
* **Framework:** FastAPI (Python 3.12)
* **Database:** MySQL 8.0 with SQLAlchemy ORM
* **Real-time:** WebSockets (for active user monitoring)
* **Containerization:** Docker & Docker Compose
* **Configuration:** Pydantic V2 (Settings & Schema validation)

## 🚀 Quick Start (Docker)

### 1. Environment Setup
Create a `.env` file in the root directory:
```env
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
JWT_SECRET=
ADMIN_PASSWORD=
```

### 2. Build & Run
Spin up the entire environment (API + Database + Frontend) with a single command (this requires to have the frontend repository [https://github.com/jkluwa/matma] cloned in the same directory as backend):
```bash
docker-compose up --build
```

### 3. Access the API and Frontend
* **Interactive Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Web UI (Frontend):** [http://localhost:3000/](http://localhost:3000/)

## 🗺️ Known Limitations

- Implement `POST /submit-answer` endpoint to determine the winner of each pair.
- Global Error Handling middleware.
