import httpx

async def Fetch_live_data(state):
    async with httpx.AsyncClient(timeout= 3.0) as client:
        try:
            response = await client.get("http://localhost:8000/sensor")
            data = response.json()
        
        except httpx.ReadError:
            data = {"error": "ESP32 unrechable"}
        
        
        return {"raw": data}






    

    