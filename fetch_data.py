from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from itertools import cycle

app= FastAPI(title="Air Monitoring API", version="1.0.0")

#read file
with open('sensor_data.json', 'r') as file:
    sensor_records= json.load(file)

# create an infinite iterator over the sensor records
sensor_iter = cycle(sensor_records)

# get data from sensors
@app.get("/sensor")
async def get_sensor_data():

    if sensor_records is None or len(sensor_records) == 0:
        return JSONResponse(status_code=404, content={"message": "No sensor data found"})
    else:
        # record = sensor_records.pop(0)
        
        # get the next record from the infinite iterator
        record= next(sensor_iter)
        return JSONResponse(status_code=200, content=record)

