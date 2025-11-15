from typing import TypedDict, Optional, Dict, List

class State(TypedDict, total= False):
    raw: Optional[Dict]
    valid: Optional[Dict]
    advice: Optional[str]
    logs: List[str]

