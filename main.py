import asyncio
from graph import app

async def main():
    initial_state= {}
    final_state= await app.ainvoke(initial_state)
    print("Final State:", final_state)


if __name__ == "__main__":
    asyncio.run(main())
    

