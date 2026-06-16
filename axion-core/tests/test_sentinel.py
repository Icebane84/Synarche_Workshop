import sys
from pathlib import Path

import pytest

# Ensure the workspace root is in the path to import forge modules
WORKSPACE_ROOT = Path(__file__).parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

from forge.sentinel import CodeSentinel


@pytest.fixture
def sentinel():
    """Provide a fresh, cache-flushed CodeSentinel for each test."""
    return CodeSentinel(use_cache=False, flush_cache=True)


def test_security_risks(sentinel):
    code = "eval('1 + 1')\nexec('x = 2')"
    sentinel._check_security_risks(Path("dummy.py"), code)
    assert len(sentinel.issues_found) == 2
    assert all(issue["rule"] == "SECURITY_RISK" for issue in sentinel.issues_found)


def test_mutable_defaults(sentinel):
    code = "def process_data(items=[]):\n    pass\n\ndef clean_data(mapping={}):\n    pass"
    sentinel._check_mutable_defaults(Path("dummy.py"), code)
    assert len(sentinel.issues_found) == 2
    assert all(issue["rule"] == "MUTABLE_DEFAULT" for issue in sentinel.issues_found)


def test_boolean_traps(sentinel):
    code = "initialize_system(True, False)"
    sentinel._check_boolean_traps(Path("dummy.py"), code)
    assert len(sentinel.issues_found) == 2
    assert all(issue["rule"] == "BOOLEAN_TRAP" for issue in sentinel.issues_found)


def test_deep_nesting(sentinel):
    code = """
def complex_logic():
    if a:
        for b in c:
            while d:
                if e:  # 4th level, should trigger
                    pass
"""
    sentinel._check_deep_nesting(Path("dummy.py"), code)
    assert len(sentinel.issues_found) == 1
    assert sentinel.issues_found[0]["rule"] == "DEEP_NESTING"


def test_global_mutable_state(sentinel):
    code = "GLOBAL_LIST = []\nGLOBAL_DICT = {}"
    sentinel._check_global_mutable_state(Path("dummy.py"), code)
    assert len(sentinel.issues_found) == 2
    assert all(issue["rule"] == "GLOBAL_MUTABLE_STATE" for issue in sentinel.issues_found)

    # Ensure __all__ is ignored
    valid_code = "__all__ = ['A', 'B']"
    sentinel._check_global_mutable_state(Path("dummy_valid.py"), valid_code)
    assert len(sentinel.issues_found) == 2  # Count shouldn't increase


def test_mutable_class_vars(sentinel):
    code = "class Configuration:\n    settings_list = []\n    mapping = {}"
    sentinel._check_mutable_class_vars(Path("dummy.py"), code)
    assert len(sentinel.issues_found) == 2
    assert all(issue["rule"] == "MUTABLE_CLASS_VAR" for issue in sentinel.issues_found)
