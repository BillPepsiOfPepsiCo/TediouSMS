import asyncio

async def hello_world():
	print("I fucking hate Python")
	
asyncio.get_event_loop().run_until_complete(hello_world())