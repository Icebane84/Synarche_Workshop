# cse/validators package
# LawValidator lives in a dot-separated RNC filename that Python cannot import
# directly via normal syntax. We load it by file path using importlib.util.
import importlib.util
import os

_file = os.path.join(os.path.dirname(__file__), "GVRN.LawValidator.CODE.py")
_spec = importlib.util.spec_from_file_location("_law_validator", _file)
_law_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_law_mod)  # type: ignore[union-attr]

LawValidator = _law_mod.LawValidator

__all__ = ["LawValidator"]
