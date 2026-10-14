# mini-rag

A minimal **RAG (Retrieval-Augmented Generation)** API for question answering, built with **FastAPI**.

Built step-by-step following [Abu Bakr Soliman's mini-rag course](https://github.com/bakrianoo/mini-rag) — one git branch per tutorial (`tut/001`, `tut/002`, …) — with my own upgrades on top (latest package versions, `uv` instead of `pip`/`conda`, extra tooling).

---

## Tech stack

| Tool | Why |
|------|-----|
| [uv](https://docs.astral.sh/uv/) | Python + package manager (replaces `pip`, `venv`, `conda`, `pip-tools`) — very fast, reproducible via `uv.lock` |
| Python **3.12** | Pinned in `.python-version` (uv downloads it automatically) |
| FastAPI | Web framework |
| Uvicorn | ASGI server that runs the FastAPI app |
| python-multipart | File uploads in FastAPI |
| pydantic-settings + python-dotenv | Load config from `.env` |
| Ruff (dev) | Linter + formatter |

---

## Requirements

- `git`
- `uv` (it will install the right Python version for you — no conda needed)

### Install on Arch Linux / CachyOS / EndeavourOS (what I use)

```bash
sudo pacman -Syu --needed git uv
uv --version
```

> **Using conda too?** If your shell auto-activates conda `(base)`, turn it off so it doesn't fight with the project's `.venv`:
> ```bash
> conda config --set auto_activate_base false
> ```
> (then open a new terminal)

### Install on other systems

```bash
# Ubuntu / Debian / WSL / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Installation

```bash
# 1) Clone
git clone https://github.com/yousefJooX/mini-rag-.git mini-rag
cd mini-rag

# 2) Create .venv + install Python 3.12 + all packages (exact versions from uv.lock)
uv sync

# 3) Environment variables
cp .env.example .env
```

Then open `.env` and fill in your own values (API keys etc.). `.env` is git-ignored — **never commit it**.

| Variable | Description |
|----------|-------------|
| `APP_NAME` | Application name |
| `APP_VERSION` | Application version |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `NVIDIA_API_KEY` | Your NVIDIA NIM API key |

> Whenever you add a new variable to `.env`, add it to `.env.example` too (with a fake value).

---

## Run the server

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

- API: http://localhost:5000/welcome
- Interactive docs (Swagger): http://localhost:5000/docs

`uv run` uses the project's `.venv` automatically — no need to activate anything.
If you still want to activate it manually:

```bash
source .venv/bin/activate        # bash / zsh
source .venv/bin/activate.fish   # fish
```

---

## Managing packages with uv (cheat sheet)

| Task | Command |
|------|---------|
| Add a package (latest version) | `uv add <package>` |
| Add a dev-only tool | `uv add --dev <package>` |
| Remove a package | `uv remove <package>` |
| See which packages are outdated | `uv tree --outdated --depth 1` |
| Upgrade **everything** to latest | `uv lock --upgrade && uv sync` |
| Upgrade one package | `uv lock --upgrade-package <package> && uv sync` |
| Install exactly what's in the lock | `uv sync --locked` |
| Run any command inside the env | `uv run <cmd>` |
| Lint / format | `uv run ruff check .` / `uv run ruff format .` |

**Versioning rule:** `pyproject.toml` holds the packages, `uv.lock` pins the **exact** version of every package (including sub-dependencies). Always commit both.

### `requirements.txt` (for pip / Docker users only)

It is generated from `uv.lock` — don't edit it by hand. After adding/upgrading packages, regenerate it:

```bash
uv export --no-hashes --no-dev --no-emit-project -o requirements.txt
```

Without uv:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

---

## Optional: nicer terminal prompt

```bash
# bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

---

## Project progress

| Branch | Topic | My upgrades |
|--------|-------|-------------|
| `tut/001` | Project boilerplate: `.gitignore`, LICENSE, README, `.env.example`, `assets/` | — |
| `tut/002` | Requirements + first FastAPI endpoint | Switched to `uv` (`pyproject.toml` + `uv.lock`), latest package versions, Python 3.12, Ruff, Arch setup docs |

## License

[Apache 2.0](LICENSE)
