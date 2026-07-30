# Talent Lens

**See Beyond the Resume.** AI-powered hiring intelligence for modern recruiting teams.

Talent Lens is a full-stack recruitment platform that uses a multi-agent LLM pipeline (LangGraph + LangChain) to parse resumes, match candidates against job requirements, score applicants, and assist with AI-driven interviews — backed by a FastAPI/PostgreSQL API and a Next.js frontend.

---

## Tech Stack

**Backend**
- FastAPI (async) + Uvicorn
- SQLAlchemy 2.0 (async ORM) + Alembic (migrations)
- PostgreSQL + asyncpg
- LangChain + LangGraph + Google Gemini (AI agent layer)
- JWT auth (access + refresh tokens)

**Frontend**
- Next.js 15 (App Router) + React 19 + TypeScript
- Tailwind CSS + Radix UI primitives
- TanStack Query + Axios
- React Hook Form + Zod
- Recharts, Framer Motion

---

## Project Structure

```
Talent Lens/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # auth, jobs, candidates, resumes, interviews, workflow
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── services/         # business logic
│   │   ├── repositories/     # data access layer
│   │   ├── database/         # engine, session, declarative base
│   │   ├── core/             # config, security, constants
│   │   └── main.py           # FastAPI app entrypoint
│   ├── ai_agents/            # LangGraph hiring pipeline (parser, matcher, scoring, decision, interview, email agents)
│   ├── alembic/               # database migrations
│   ├── tests/
│   ├── requirements.txt
│   └── .env                  # local secrets — never commit
│
└── frontend/
    ├── app/                   # Next.js App Router pages
    │   ├── (auth)/            # login, register, forgot/reset password
    │   └── (dashboard)/       # dashboard, jobs, candidates, analytics, etc.
    ├── components/            # UI primitives, dashboard widgets, layout, auth
    ├── lib/
    │   ├── api/                # typed API client + service layer per resource
    │   ├── hooks/               # TanStack Query hooks
    │   ├── providers/           # auth, theme, query context
    │   └── types/                # TypeScript types mirroring backend schemas
    └── .env.local              # local config — never commit
```

---

## Prerequisites

| Tool | Version | Check with |
|---|---|---|
| Python | 3.11+ | `python --version` |
| Node.js | 20+ (LTS) | `node -v` |
| PostgreSQL | 14+ | `psql --version` |

On Windows, if `psql` or `node` aren't recognized, they're likely installed but not on your PATH — see [Troubleshooting](#troubleshooting) below.

---

## Backend Setup

```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1          # Windows PowerShell
# source venv/bin/activate         # macOS/Linux

pip install -r requirements.txt
```

### 1. Configure environment variables

Copy `.env.example` to `.env` and fill in real values:

```dotenv
ENVIRONMENT=development

# Real Postgres credentials — not the placeholder user:password
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/hiring_ai

# Generate with: python -c "import secrets; print(secrets.token_urlsafe(64))"
JWT_SECRET_KEY=your-generated-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES=30

UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE_MB=10

# AI agent layer — get a key from Google AI Studio
GOOGLE_API_KEY=your-google-api-key
GEMINI_MODEL=gemini-2.5-flash
LLM_TEMPERATURE=0.2
```

> **Never commit `.env` or paste real secrets anywhere outside your local machine.** If a key is ever exposed (chat, screenshot, git history), rotate it immediately in Google Cloud Console.

### 2. Create the database

```powershell
psql -U postgres -c "CREATE DATABASE hiring_ai;"
```

### 3. Run migrations

```powershell
alembic upgrade head
```

### 4. Start the server

```powershell
uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to confirm the API is running (interactive Swagger UI).

---

## Frontend Setup

```powershell
cd frontend
npm install
```

### 1. Configure environment variables

Copy `.env.example` to `.env.local`:

```dotenv
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 2. Start the dev server

```powershell
npm run dev
```

Visit `http://localhost:3000`. You should be redirected to `/login`; register a new account to reach the dashboard.

---

## Running Both Together

Two terminals, both left running:

```powershell
# Terminal 1
cd backend
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload

# Terminal 2
cd frontend
npm run dev
```

CORS is pre-configured on the backend to allow `http://localhost:3000` by default (`cors_allow_origins` in `app/core/config.py`).

---

## Key API Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/auth/register` | Create account, returns user + token pair |
| POST | `/api/v1/auth/login` | Authenticate, returns token pair |
| POST | `/api/v1/auth/refresh` | Exchange refresh token for new access token |
| GET | `/api/v1/auth/me` | Current authenticated user |
| GET/POST | `/api/v1/jobs` | List / create jobs |
| GET/PUT/DELETE | `/api/v1/jobs/{id}` | Manage a single job |
| GET | `/api/v1/candidates?job_id=` | List candidates for a job |
| POST | `/api/v1/resumes/upload` | Upload + parse a resume |
| POST | `/api/v1/interview/questions` | Generate next interview question |
| POST | `/api/v1/interview/evaluate` | Evaluate interview transcript |
| POST | `/api/v1/workflow/evaluate` | Run the full AI hiring workflow for a candidate |

Full interactive reference: `http://127.0.0.1:8000/docs`.

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'app'`**
You're running `uvicorn` from the wrong directory. Run it from inside `backend/`, not the project root:
```powershell
cd backend
uvicorn app.main:app --reload
```

**`Connect call failed ... port 5432`**
PostgreSQL isn't running, or `DATABASE_URL` in `.env` still has placeholder credentials (`user:password`). Confirm Postgres is running and use your real password.

**`psql: command not found` (Windows)**
Postgres's `bin` folder isn't on PATH. Either call it by full path:
```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres
```
or add `C:\Program Files\PostgreSQL\18\bin` to your system PATH and restart the terminal.

**`npm: command not found`**
Node.js isn't installed. Download the LTS installer from [nodejs.org](https://nodejs.org), then restart your terminal.

**`asyncpg.exceptions.DuplicateObjectError: type "user_role" already exists`**
A known Alembic/SQLAlchemy enum-DDL conflict — the ORM models and the migration both attempted to create the same Postgres enum type. Fixed by setting `create_type=False` on every `Enum`/`ENUM` definition (both in `app/models/*.py` and `alembic/versions/0001_initial.py`), so only the migration's explicit `.create()` call owns type creation.

**Frontend shows "Network Error" on every request**
The backend isn't running, or `NEXT_PUBLIC_API_URL` in `frontend/.env.local` doesn't match where it's actually listening. Restart `npm run dev` after changing `.env.local` — Next.js only reads it at startup.

---

## Security Notes

- Rotate any API key or secret immediately if it's ever pasted into a chat, screenshot, commit, or shared document.
- `.env` and `.env.local` are git-ignored by default — keep it that way.
- JWT secrets should be freshly generated per environment (dev, staging, prod), never reused.

---

## License

Internal project — not licensed for external distribution.
