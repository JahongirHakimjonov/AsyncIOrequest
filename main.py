import asyncio
import json

import aiohttp


async def get_names_data(names):
    api_url = 'https://api.agify.io'
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = [get_name_data(session, api_url, name) for name in names]
        results = await asyncio.gather(*tasks)

    return results


async def get_name_data(session, api_url, name):
    url = f'{api_url}?name={name}'
    async with session.get(url) as response:
        data = await response.json()
        return {'name': name, 'age': data['age']}


async def append_to_json_file(results, filename='names.json'):
    try:
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    combined_data = existing_data + results

    with open(filename, 'w') as file:
        json.dump(combined_data, file, indent=2)

    print(f"Yangi malumotlar '{filename}' fayliga qo'shildi.")


async def main():
    input_names = list(map(str, input("Ismlar kiriting (bo'sh joy bering): ").split()))
    results = await get_names_data(input_names)
    await append_to_json_file(results)


asyncio.run(main())
