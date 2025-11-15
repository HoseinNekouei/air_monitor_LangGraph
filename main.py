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
    print("Final State:", final_state)


if __name__ == "__main__":
    asyncio.run(main())


