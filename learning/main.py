import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import json
import requests

ollamaURL = "https://ollama.vndev.online/api/generate"

async def main():
    # browser_config = BrowserConfig()  # Default browser configuration
    # run_config = CrawlerRunConfig()   # Default crawl run configuration

    # async with AsyncWebCrawler(config=browser_config) as crawler:
    #     result = await crawler.arun(
    #         url="https://example.com",
    #         config=run_config
    #     )
    #     print(result.markdown)  # Print clean markdown content
    with open("data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        # Access and print the content
    
    # print(data['products'])

    req = {
        "model": "deepseek-r1:1.5b",
        "prompt": (
            "hello world"
            # "find the max price in data list i provided. result should is only a number as the max price. example the result is 99.88. this is the data : " + str(data['products'])
        ),
        "format": "json",
        "stream": False
    }
    response = requests.post(ollamaURL, json=req)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response received successfully:")
        print(response.json()['response'])  # Parse and print the JSON response
    else:
        print(f"Failed to get response. Status code: {response.status_code}")



if __name__ == "__main__":
    asyncio.run(main())
