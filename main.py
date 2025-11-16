from graph import app_graph
from state import State
from fastapi import FastAPI
from fastapi.responses import JSONResponse


app= FastAPI()

@app.get('/')
async def main():
    initial_state: State= {
        'raw': None,
        'valid': None,
        'advice': None,
        'logs': []
    }

    final_state= await app_graph.ainvoke(initial_state)

    # # Access final state components
    # print("Final Advice:", final_state.get('advice'))
    # print("Logs:", final_state.get('logs'))

    return JSONResponse(
            status_code=200, 
            content= {
                'Final Advice': final_state.get('advice'),
                'Logs': final_state.get('logs') 
                }
             )


