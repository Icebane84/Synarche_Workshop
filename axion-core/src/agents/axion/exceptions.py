"""
### **Block A: The Identification Lock (UIP-V15)**
ID: AXION-EXCEPTIONS-001
Official Name: exceptions.py
Version: v15.0 [OMEGA]
Domain: AXION
Status: [ACTIVE]
Ethos: "Dissonance Captured. Errors Handled."
Relations: IDENTITY: High Priestess | The Sovereign.
"""

class AxionError(Exception):
    """Base class for all Axion-related dissonance."""
    pass


class SovereignViolation(AxionError):
    """Raised when a core OMEGA principle or governance rule is violated."""
    pass


class ArmoryError(AxionError):
    """Raised when tools in the Seven-Agent Matrix are missing or broken."""
    pass


class CognitionDissonance(AxionError):
    """Raised when the NLP or retrieval engine fails to decode intent."""
    pass
