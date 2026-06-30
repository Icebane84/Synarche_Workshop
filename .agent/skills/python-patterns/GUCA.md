# GUCA: Python Command Registry [v15.0]

## 🛠️ Audit Commands

### 🔍 API & Type Integrity
- `/audit_pydantic_models` - Scan for Pydantic v2 compliance and schema validation gaps.
- `/verify_type_hints` - Check all function signatures and return types for mandatory hinting.
- `/validate_django_orm` - Scan for N+1 query risks and missing `select_related()` calls.

### 🚀 Performance & Concurrency
- `/audit_async_hygiene` - Check for blocking `requests` or `time.sleep` in `async` code.
- `/verify_concurrency_model` - Analyze thread/process usage for CPU-bound tasks.
- `/check_uvicorn_config` - Validate deployment settings for FastAPI/Starlette.

### 🛡️ Security Guardrails
- `/audit_python_security` - Check for SQL concatenation, shell execution (`os.system`), and hardcoded secrets.
- `/verify_venv_isolation` - Check dependency hygiene and virtual environment constraints.
- `/check_csrf_cors` - Validate Django/FastAPI security middleware.


### 🛡️ Final Verification
- `/omega_audit` - Execute the master cluster-wide validation script.
  - **Automation**: `python scripts/omega_audit.py`

---
**Usage**: These commands are to be executed as part of the **Python Pre-Work Validation** or **In-Depth System Audit** phases of any Python task. Use with the **AOP.md** playbook as authority.
