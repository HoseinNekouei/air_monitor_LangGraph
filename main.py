import asyncio
from graph import app
from state import State

async def main():
    initial_state: State= {
        'raw': None,
        'valid': None,
        'advice': None,
        'logs': []
    }

    final_state= await app.ainvoke(initial_state)

    # Access final state components
    print("Final Advice:", final_state.get('advice'))
    print("Logs:", final_state.get('logs'))



if __name__ == "__main__":
    asyncio.run(main())


