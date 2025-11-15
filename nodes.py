import httpx
from datetime import datetime


#-------------------- 1. Fetch Node---------------------------------------------
async def fetch_data_node(state):
    async with httpx.AsyncClient(timeout= 3.0) as client:
        try:
            response = await client.get("http://localhost:8000/sensor")
            data = response.json()
        
        except httpx.ReadError:
            data = {"error": "ESP32 unrechable"}
        
        
        return {"raw": data}
    

#----------------------2. Validation Node ---------------------------------------
def validate_node(state):
    raw = state.get("raw")
    
    # Check for error or None
    if raw is None or isinstance(raw, dict) and 'error' in raw:
        return {'valid': None}
    
    # Check if raw data is empty or not dict
    if not isinstance(raw, dict) or not raw:
        return {'valid': None}
    
    # Define required fields and their types
    required_fields = {
        'temperature': (float, int),
        'humidity': (float, int),
        'gas': (float, int),
    }

    import pdb
    pdb.set_trace()
    
    # Validate each required field
    for field, expected_types in required_fields.items():
        if field not in raw:
            return {'valid': None}
        
        value = raw[field]
        
        # Check if value is of correct type
        if not isinstance(value, expected_types):
            return {'valid': None}
        
        # Check if value is not NaN
        if isinstance(value, float) and value != value:
            return {'valid': None}
    
    # Range validation for sensor values
    if not (-50 <= raw['temperature'] <= 100):
        return {'valid': None}
    
    if not (0 <= raw['humidity'] <= 100):
        return {'valid': None}
    
    if raw['gas'] < 0:
        return {'valid': None}
    
    return {'valid': raw}


#---------------------------------------3. Analyze Node ----------------------------
def analyze_node(state):
    valid = state.get('valid')

    if valid is None:
        return {'advice': 'NO VALID DATA AVAILABLE !'}

    temperature = valid["temperature"]
    humidity = valid["humidity"]
    gas = valid['gas']

    if temperature > 30 and humidity < 40:
        msg = "Air is hot and dry. Consider improving ventilation."
    
    elif temperature < 15:
        msg = "Air is too cold."
    
    elif gas > 400:
        msg= "The air is polluted, open the window."

    else:
        msg = "Conditions are normal."

    return {"advice": msg}    


#------------------------------------ 4. Logger Node --------------------------------
def logger_node(state):

    log_entry= f"{datetime.now()} | raw= {state.get('raw')} | advice= {state.get('advice')}"

    logs= state.get('logs', [])
    logs.append(log_entry)

    return {'logs': logs}




