from algoliasearch.search.client import SearchClientSync
import asyncio
import json  # Import the json module

client = SearchClientSync("DN83H0EFK4", "dab20c5dad503493810a3cd2b65e11f5")

async def search(query: str):
    results = client.search(
        {
            "requests": [
                {
                    "indexName": "flomaster-chrsnv",
                    "query": query  # Use the query parameter
                }
            ]
        }
    )

    results_json_string = results.model_dump_json()  # Get the JSON string
    results_dict = json.loads(results_json_string)  # Parse the JSON string into a dictionary

    print(results_dict)
    return results_dict  # Return the dictionary


async def main():
    query = "доступность подписок" #Use your query
    results = await search(query)
    print(results)
    if results and results['results'] and results['results'][0]['hits']: # Check if results and hits exist
        print(f"""Запрос: {results['results'][0]["query"]}

Заголовок: {results['results'][0]['hits'][0]["anchor"]}
URL: {results['results'][0]['hits'][0]["url"]}""")
    else:
        print("Search failed or no results found.")


if __name__ == "__main__":
    asyncio.run(main())