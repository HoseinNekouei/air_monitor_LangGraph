from typing import TypedDict, Optional, Dict, List

class SensorState(TypedDict, total= False):
    raw: Optional[Dict]
    valid: Optional[Dict]
    advice: Optional[str]
    logs: list[str]

