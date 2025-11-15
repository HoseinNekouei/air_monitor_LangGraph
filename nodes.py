import httpx
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

import os

load_dotenv()

# Initialize OpenAI client with .env variables
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

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
    You are an environmental monitoring assistant.

    Sensor data:
    temperature={data['temperature']} °C
    humidity={data['humidity']} %
    gas={data['gas']} ppm

    Return ONLY:
    A single short sentence (max 20 words) giving practical advice.
    No lists, no formatting, no headings, no markdown, no explanations.
    If data is normal, still give one simple recommendation.
    Output must be plain text only.
    """    

    try:
        response= client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an air quality and temperature advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens= 100,
            n= 1,
            stop= None,
            temperature= 0.7,
        )

        advice= response.choices[0].message.content
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




