import httpx
import openai
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


#------------------------------------ 3. Advice Node --------------------------------
def advice_node(state):
    if not state.get('valid'):
        return {'advice': 'NO VALID DATA AVAILABLE !'}
    
    data = state['valid']
    
    prompt = f"""
    You are an air quality and temperature advisor.
    Given the following sensor readings:
    - Temperature: {data['temperature']} °C
    - Humidity: {data['humidity']} %
    - Gas level: {data['gas']}
    Provide clear advice in natural language for actions to improve comfort and safety.
    """    

    try:
        response= openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens= 60,
            n= 1,
            stop= None,
            temperature= 0.7,
        )
        advice= response.choices[0].message['content'].strip()
        state['advice']= advice

    except Exception as e:
        return {'advice': f"Error generating advice: {str(e)}"}
    
    return {'advice': state['advice']}
    
#------------------------------------ 4. Logger Node --------------------------------
def logger_node(state):

    log_entry= f"{datetime.now()} | raw= {state.get('raw')} | advice= {state.get('advice')}"

    logs= state.get('logs', [])
    logs.append(log_entry)

    return {'logs': logs}




