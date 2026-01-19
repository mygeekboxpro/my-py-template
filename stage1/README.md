# Title

---

## macOS (Intel) — Run Instructions

### Prerequisites
- macOS (Intel)
- uv installed
- Python 3.11+

### Required env vars:

## Environment Configuration
### File: `.env.example`
```env
ENV_TYPE=development

# OpenAI (optional for live model; tests do not require this)
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini

HTTP_TIMEOUT_SECONDS=10

# sqlite
APP_DB_PATH=./data/app.db
TENANT_ID=tenant_demo


#------------------------------------------------------------------------------
# BEGIN: DEV ONLY CONFIG
#------------------------------------------------------------------------------

# json  (default, production-safe),
# true  (adds blank line between logs (dev only))
# prety (pretty + blank line (local development))
LOG_LEVEL=INFO
LOG_MODE=pretty
LOG_PRETTY=true
```

---


## Setup (Follow in Order)

### 1. Verify CPU architecture
```bash
uname -m
```
#### Expected 
- x86_64


### 2. Verify `uv`
```bash
which uv
uv --version
```

#### If missing, run 
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
#### Restart terminal after install.


### 3. Create virtual environment

#### a. Clone / enter project directory
```bash
cd stage1
```
#### Directory must contain:
- pyproject.toml
- src/
- scripts/
- tests/

### b. Copy environment variables
```bash
cp .env.example .env
```

### c. Enable environment variables
```bash
set -a
source .env
set +a
```

#### b. Install `.venv`
```bash
rm -rf .venv
uv venv
```

#### c. Activate `.venv`
```bash
source .venv/bin/activate
```

#### d. Verify Python
```bash
which python
uv run python --version
```
#### Expected
- .../stage1/.venv/bin/python
- Python 3.11.14


### 4. Install dependencies
```bash
uv pip install -e ".[dev]"
```
#### Expected
- No errors
- mcp, fastapi, uvicorn, httpx installed


### 5. Install `pyyaml` (for prompt-composer)
```bash
set -a
source .env
source .venv/bin/activate
set +a
uv pip install pyyaml
```

### Terminal 1 — Run script
```bash
set -a
source .env
source .venv/bin/activate
# chmod +x scripts/{file_name}.sh
set +a
# ./scripts/{file_name}.sh
```

**Expected:**  
TBU


### Terminal X — Tests 
```bash
set -a
source .env
source .venv/bin/activate
set +a
uv run pytest -q
```
#### Expected:
- All tests pass.
#### Tests include:
- Unit test: 
- Integration test: 


## Clean shutdown
 In all terminals:
```bash
ctrl+C
```
#### Order does not matter.


## 📌 FAQ

---

## 📌Troubleshooting: Common failure symptoms & fixes
