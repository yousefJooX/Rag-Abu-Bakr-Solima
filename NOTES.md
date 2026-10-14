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