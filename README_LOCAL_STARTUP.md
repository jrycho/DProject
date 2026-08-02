# Local Startup

This project has a FastAPI backend, a MongoDB database, and a Next.js frontend.

## Prerequisites

- Python 3.11
- Node.js 20
- npm
- Docker Desktop, if using the Docker workflow

## Environment

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Edit `.env` before starting the app:

- `MONGO_URI`: Mongo connection string. Use `mongodb://localhost:27017` for a local MongoDB instance, or `mongodb://mongo:27017` inside Docker Compose.
- `MONGO_DB_NAME`: database name, normally `nutrition_app`.
- `SECRET_KEY`: required for JWT signing. Use a long random value.
- `DOMAIN`: frontend URL used in password reset links, normally `http://localhost:3000`.
- `SMTP_*`: email settings for the forgotten-password flow. `SMTP_PASS` can stay empty if you do not use password reset emails locally.
- `NEXT_PUBLIC_API_URL` and `NEXT_PUBLIC_API_BASE`: frontend API base URL, normally `http://localhost:8000` for manual local startup.

## Option 1: Docker Backend and MongoDB

Start FastAPI and MongoDB:

```powershell
docker compose -f docker-compose.dev.yml up --build
```

Backend URL:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

Then start the frontend in another terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:3000
```

## Option 2: Manual Backend, MongoDB, and Frontend

Start MongoDB locally first. The backend expects:

```text
mongodb://localhost:27017
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r requirements.txt
```

Start the backend:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Start the frontend in another terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Useful Commands

Run backend tests:

```powershell
pytest
```

Build the frontend:

```powershell
Set-Location frontend
npm run build
```

Stop Docker services:

```powershell
docker compose -f docker-compose.dev.yml down
```
