import asyncio
from mealieapi import MealieClient


client = MealieClient("<YOUR_MEALIE_SERVER_ADDRESS>")

async def main():
    client.authorize("<API_KEY>")
    client.create_recipe_from_url()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())