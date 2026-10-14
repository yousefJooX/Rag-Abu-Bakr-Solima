# mini-rag — Course Notes
> Notes I take while following the course, plus things I searched/learned on my own.

---

## Tutorial 001 — Project Boilerplate

### Git workflow
- One branch per tutorial: `tut/001`, `tut/002`, ...
- Branch naming matters. Teams use prefixes like `feature/...` or `fix/...`, or the Jira task ID.
- Commit after every small change. It becomes a habit.
- Finish the tutorial → merge into `main` → push.

### Essential files
| File | Purpose |
|------|---------|
| `.gitignore` | Files git should NOT track (cache, data, `.env`, `.venv`). Template from github/gitignore → Python |
| `LICENSE` | Project license (Apache 2.0) |
| `README.md` | The project's front door. Explain EVERYTHING as if the reader doesn't know Python |
| `.env` | Config + secrets (API keys). **Never commit it** |
| `.env.example` | Copy of `.env` with fake values. This is what gets committed |
| `assets/.gitkeep` | Keeps an empty folder tracked by git (opposite of `.gitignore`) |

### Config rules
- Env variable names are UPPER_SNAKE_CASE constants: `APP_NAME`, `OPENAI_API_KEY`.
- Values are strings or numbers.
- Every time you add a variable to `.env`, add it to `.env.example` too.
- A new developer runs `cp .env.example .env` and fills in their own values.

### Tip
- Always leave an empty line at the end of a file. Otherwise git shows a fake diff on the previous line.

---

## Tutorial 002 — Requirements & First FastAPI App

### FastAPI vs Uvicorn
- **FastAPI**: the web framework (routes, validation, docs). It pushes you to write standard code.
- **Uvicorn**: the ASGI **server** that actually runs the app and listens on a port.
- In production, uvicorn alone isn't enough. Put **Nginx** in front of it as a reverse proxy.
- **python-multipart**: needed for file uploads in FastAPI.

### Run the server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
- `main:app` means the file `main.py` and the variable `app = FastAPI()`.
- `--reload` restarts the server automatically when the code changes. Use it in dev only.
- `--host 0.0.0.0` makes the server reachable from other devices on the network.
- `--port 5000` changes the port (the default is 8000).
- `python main.py` does NOT start the server. Use uvicorn.
- Stop with **Ctrl+C**. Ctrl+Z only pauses it, so the port stays busy (`Address already in use`). Fix: `kill %1`.

### URLs
- `/welcome` is my endpoint.
- `/docs` is Swagger UI, auto-generated. You can test every endpoint from here.
- `/redoc` is the same docs in another style.
- `404` on `/` is normal, because no route is defined for it.

### Pin versions! 📌
- Never put a package in requirements without a version. Otherwise the latest gets installed and may break the code.
- Get the version from pypi.org.

### uv (my upgrade) ⚡
Replaces pip + venv + conda + pip-tools. Written in Rust, so it's very fast.

| Task | Command |
|------|---------|
| Install everything (new `.venv`) | `uv sync` |
| Install into my conda env | `uv pip install -r requirements.txt` |
| Add a package | `uv add <pkg>` |
| Add a dev tool | `uv add --dev <pkg>` |
| Remove | `uv remove <pkg>` |
| Show outdated | `uv tree --outdated --depth 1` |
| Upgrade everything | `uv lock --upgrade` |
| Regenerate requirements | `uv export --no-hashes --no-dev --no-emit-project -o requirements.txt` |
| Run inside env | `uv run <cmd>` |

- `pyproject.toml` holds the package names. `uv.lock` holds the exact pinned versions. Commit both.
- Don't use `uv sync` with conda. It deletes packages that aren't in the lock.

---

## 🔍 Things I searched on my own

### Postman vs FastAPI `/docs`
- `/docs` is quick for testing the endpoints of a single app.
- **Postman** is a full API client. It saves requests, environments, and auth.
- **Postman Collection** is a group of saved requests. Export it as JSON or share a link, and a teammate can run the same tests.
- Alternatives: **Bruno** (open-source, stores requests as files inside the repo), Insomnia, and the **Thunder Client / REST Client** extensions in VS Code.

---

## 💡 Ideas to apply in my graduation project (legal RAG)
- Same structure: `.env` + `.env.example`, `uv`, one branch per feature.
- Use `/docs` to demo the API to the supervisor.

---

## Tutorial 003 — Nested Routes + Env Values

### Why split routes out of `main.py`?
- Putting every endpoint in `main.py` turns it into one huge file that's hard to maintain.
- Split by responsibility: every group of endpoints lives in its own file inside `routes/`.
- `main.py` only creates the app and **includes** the routers.

### Make `routes/` a Python package
- Add an empty `routes/__init__.py`, so Python treats the folder as a package you can import from.

```
routes/
├── __init__.py
└── base.py      ← base_router (welcome endpoint)
```

### `APIRouter`: a mini app for a group of endpoints
```python
from fastapi import APIRouter

base_router = APIRouter(
    prefix="/api/v1",   # added before every route in this router
    tags=["api_v1"],    # group name in /docs (Swagger)
)

@base_router.get("/")   # final path = /api/v1/
def welcome():
    ...
```
And in `main.py`:
```python
from routes import base
app.include_router(base.base_router)
```

| Param | What it does |
|-------|--------------|
| `prefix` | Default path before all routes in the router. `"/"` becomes `/api/v1/`. **Must start with `/`**, otherwise `AssertionError: A path prefix must start with '/'` |
| `tags` | Groups endpoints in `/docs`. Easy to rename later in one place |

- **Why `/api/v1`?** That's **API versioning**. If the API changes in a breaking way, add `/api/v2` and old clients keep working on v1.
- Both import styles work: `from routes import base` (the instructor's, nicer with many routers) or `from routes.base import base_router` (mine, more direct).

### Read values from `.env` instead of hardcoding
- Goal: the welcome response shows the app name, version and author from `.env`, not a hardcoded string.
```python
# main.py — load .env BEFORE importing routes
from dotenv import load_dotenv
load_dotenv(".env")

from routes import base
```
```python
# routes/base.py
import os
app_name = os.getenv("APP_NAME")
```
- `load_dotenv()` copies the `.env` values into the environment variables, then `os.getenv()` reads them.
- **Order matters:** call `load_dotenv` before importing any module that reads env values.
- New variable in `.env` (`AUTHOR`) → also add it to `.env.example` ✅
- ⚠️ `os.getenv` returns `None` if the variable is missing, with no error. Next step: `pydantic-settings` validates config at startup.

- ✅ Tested in Postman: the response now returns the app name, author and version from `.env`.

### `async def` — FastAPI handles many requests at once
- A normal `def` endpoint blocks a worker until it finishes. `async def` lets the server handle other requests **while waiting** (DB query, LLM API call, file upload).
- Rule: use `async def` + `await` when the endpoint calls async I/O (e.g. `httpx`, async DB drivers, OpenAI async client).
- ⚠️ Don't call blocking code (e.g. `time.sleep`, `requests.get`) inside `async def`, because it freezes the whole server. Use plain `def` for that, and FastAPI runs it in a thread pool.
```python
@base_router.get("/")
async def welcome():
    ...
```

### Postman
- **Postman** is an API client: send requests, see responses, save them.
- I opened the repo in Postman **Git mode (Local View)**, so everything is saved as YAML inside the repo:
```
.postman/resources.yaml                               ← workspace ID
postman/environments/local.environment.yaml           ← environment
postman/collections/mini-rag-app/welcome.request.yaml ← requests
```
- **Environment** `local`: variable `api = http://localhost:5000`, used as `{{api}}/api/v1/`.
  - The value is stored **locally only** (not in the YAML), so secrets never go to GitHub. After cloning, set `api` yourself.
- **Collection** `mini-rag-app`: groups all the project's requests.
- Request type **HTTP** (REST), method **GET**.

### 🐛 Bugs I hit
| Error | Cause | Fix |
|-------|-------|-----|
| `{{api}}` red + `ENOTFOUND` | Variable saved as `'   api'` (spaces) + empty value | Retype the name with no spaces, set the value, Ctrl+S |
| `404 Not Found` on `/api/v1/` | Router had no `prefix` yet | Add `prefix="/api/v1"` |
| `AssertionError: A path prefix must start with '/'` | Left `prefix="___"` | Prefix must start with `/` |

### Request flow
```
Postman ─ GET {{api}}/api/v1/ ─▶ uvicorn :5000 ─▶ main.py (app)
        ─▶ base_router (/api/v1) ─▶ welcome() ─▶ 200 OK + JSON
```
