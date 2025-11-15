from typing import TypedDict, Optional, Dict

class SensorState(TypedDict):
    raw: Optional[Dict]             # raw json data from the sensor
    analysed: Optional[str]         # text analysis output

