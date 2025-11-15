import httpx


#-------------------- 1. Fetch Node---------------------------------------------
async def Fetch_live_data(state):
    async with httpx.AsyncClient(timeout= 3.0) as client:
        try:
            response = await client.get("http://localhost:8000/sensor")
            data = response.json()
        
        except httpx.ReadError:
            data = {"error": "ESP32 unrechable"}
        
        
        return {"raw": data}
    

#----------------------2. Validation Node ---------------------------------------
def validate_data(state):
    raw = state.get("raw", {})

    # check for error in raw data
    if 'error' in raw:
        return {'valid': None} # propagate error
    
    # check for raw data is empty or not dict
    if not isinstance(raw, dict) or not raw:
        return{'valid': None}
    
    # Define required fields and their validation rules
    required_fields= {
        'tempreture': (float, int),
        'humidity': (float, int),
        'gas': (float, int),
    }

    # Validate each required field
    for field, expected_types in required_fields.items():
        if field not in raw:
            return {'valid': None}
        
        value = raw[field]
        
        # Check if value is of correct type
        if not isinstance(value, expected_types):
            return {'valid': None}
        
        # Check if value is not NaN
        if isinstance(value, float) and value != value:  # NaN check
            return {'valid': None}
    
    # Add range validation for sensor values
    if not (0 <= raw['temperature'] <= 100):  # Adjust range as needed
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


    

    