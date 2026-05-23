import functools
import hashlib
import json
import logging
import sys
import time
import traceback
from pathlib import Path
import yaml
from jsonschema import validate
SCHEMA_PATH = "uip_v15.schema.json"


def synarche_audit(func: callable) -> callable:
    """Architectural wrapper for standardized logging compliance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("PhoenixLogger")
        start_time = time.perf_counter()
        logger.debug(f"Executing {func.__name__} | Args: {args}")
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            logger.info(f"Finished {func.__name__} in {duration:.4f}s")
            return result
        except Exception as e:
            logger.error(f"CRITICAL FAILURE in {func.__name__}: {e!s}\n{traceback.format_exc()}")
            raise
    return wrapper


class ConceptualIntegrityValidator:
    def __init__(self, artifact_path: str) -> None:
        self._setup_logger()
        self.artifact_path = Path(artifact_path)
        if not self.artifact_path.exists():
            raise FileNotFoundError(f"Artifact not found: {artifact_path}")
        
        self.raw_content = self.artifact_path.read_text(encoding="utf-8")
        self.metadata = self.extract_frontmatter()
        
        schema_file = Path(SCHEMA_PATH)
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema definition missing: {SCHEMA_PATH}")
        self.schema = json.loads(schema_file.read_text(encoding="utf-8"))

    def _setup_logger(self):
        self.logger = logging.getLogger("PhoenixLogger")
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def extract_frontmatter(self):
        if not self.raw_content.startswith("---"):
            raise Exception("Missing YAML frontmatter")

        parts = self.raw_content.split("---", 2)
        return yaml.safe_load(parts[1])

    @synarche_audit
    def validate_schema(self):
        validate(instance=self.metadata, schema=self.schema)

    @synarche_audit
    def validate_integrity(self):
        content_hash = hashlib.sha256(self.raw_content.encode()).hexdigest()
        self.metadata.setdefault("integrity", {})
        stored_hash = self.metadata["integrity"]["hash"]

        if stored_hash and stored_hash != content_hash:
            raise Exception("Integrity violation detected")

        self.metadata["integrity"]["hash"] = content_hash

    def generate_selt(self):
        return {
            "event": "CIV_AUDIT",
            "artifact_id": self.metadata["artifact_id"],
            "result": "PASS",
            "status": "CANONIZED",
        }

    @synarche_audit
    def audit(self) -> None:
        self.validate_schema()
        self.validate_integrity()
        selt = self.generate_selt()
        print(json.dumps(selt, indent=2))


if __name__ == "__main__":
    try:
        target = sys.argv[1] if len(sys.argv) > 1 else "UMB-DEMO-001.md"
        validator = ConceptualIntegrityValidator(target)
        validator.audit()
    except Exception as e:
        print(f"Audit Aborted: {e}")
