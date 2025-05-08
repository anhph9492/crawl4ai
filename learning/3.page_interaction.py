# ANCHOR multiple-steps interaction
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def multi_page_commits():
    browser_cfg = BrowserConfig(
        headless=False,  # Visible for demonstration
        verbose=True
    )
    session_id = "github_ts_commits"

    base_wait = """js:() => {
        const commits = document.querySelectorAll('li.Box-sc-g0xbh4-0 h4');
        return commits.length > 0;
    }"""

    # Step 1: Load initial commits
    config1 = CrawlerRunConfig(
        wait_for=base_wait,
        session_id=session_id,
        cache_mode=CacheMode.BYPASS,
        # Not using js_only yet since it's our first load
    )

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(
            url="https://github.com/microsoft/TypeScript/commits/main",
            config=config1
        )
        print("Initial commits loaded. Count:", result.cleaned_html.count("commit"))

        # Step 2: For subsequent pages, we run JS to click 'Next Page' if it exists
        js_next_page = """
        const selector = 'a[data-testid="pagination-next-button"]';
        const button = document.querySelector(selector);
        if (button) button.click();
        """

        # Wait until new commits appear
        wait_for_more = """js:() => {
            const commits = document.querySelectorAll('li.Box-sc-g0xbh4-0 h4');
            if (!window.firstCommit && commits.length>0) {
                window.firstCommit = commits[0].textContent;
                return false;
            }
            // If top commit changes, we have new commits
            const topNow = commits[0]?.textContent.trim();
            return topNow && topNow !== window.firstCommit;
        }"""

        for page in range(2):  # let's do 2 more "Next" pages
            config_next = CrawlerRunConfig(
                session_id=session_id,
                js_code=js_next_page,
                wait_for=wait_for_more,
                js_only=True,       # We're continuing from the open tab
                cache_mode=CacheMode.BYPASS
            )
            result2 = await crawler.arun(
                url="https://github.com/microsoft/TypeScript/commits/main",
                config=config_next
            )
            print(f"Page {page+2} commits count:", result2.cleaned_html.count("commit"))

        # Optionally kill session
        await crawler.crawler_strategy.kill_session(session_id)

async def main():
    await multi_page_commits()

if __name__ == "__main__":
    asyncio.run(main())



# ANCHOR Dynamic content
# import asyncio
# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
# from crawl4ai.content_filter_strategy import PruningContentFilter
# from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


# def write2MD(result,file_path):
#     # Check if the operation was successful
#     if result:
#         # Write the selected markdown content into the .md file
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write(result)
        
#         print(f"Markdown content has been written to {file_path}")
#     else:
#         print("Operation failed. No markdown content to write.")

# async def main():
#     prune_filter = PruningContentFilter(
#         # Lower → more content retained, higher → more content pruned
#         threshold=0.45,           
#         # "fixed" or "dynamic"
#         threshold_type="dynamic",  
#         # Ignore nodes with <5 words
#         min_word_threshold=5      
#     )
#     md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)

#     # Step 1: Load initial Hacker News page
#     config = CrawlerRunConfig(
#         markdown_generator=md_generator,
#         wait_for="css:.athing:nth-child(10)",  # Wait for 30 items
#     )
#     async with AsyncWebCrawler() as crawler:
#         # result = await crawler.arun(
#         #     url="https://news.ycombinator.com",
#         #     config=config
#         # )
#         # write2MD(result, 'result1.md')

#         # Re-use the same crawler session
#         result2 = await crawler.arun(
#             url="https://news.ycombinator.com",  # same URL but continuing session
#             config=CrawlerRunConfig(
#                 # js_code=[
#                 #     "window.scrollTo(0, document.body.scrollHeight);",
#                 #     # The "More" link at page bottom
#                 #     "document.querySelector('a.morelink')?.click();"  
#                 # ],
#                 # wait_for="""js:() => {
#                 #     return document.querySelectorAll('.athing').length === 30;
#                 # }""",
#                 markdown_generator=md_generator,
#                 # Mark that we do not re-navigate, but run JS in the same session:
#                 # js_only=True,
#                 session_id="hn_session"
#             )
#         )
#         # total_items = result2.cleaned_html.count("athing")
#         print("Mycoria is an open and secure overlay network that connects all participants" in result2.cleaned_html)
#         # write2MD(result2.markdown, 'result2.md')
#         # print(result2.markdown)

# if __name__ == "__main__":
#     asyncio.run(main())

##################################################################
##################################################################

# ANCHOR Basic
# import asyncio
# from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

# async def main():
#     # Single JS command
#     config = CrawlerRunConfig(
#         js_code="window.scrollTo(0, document.body.scrollHeight);"
#     )

#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             url="https://news.ycombinator.com",  # Example site
#             config=config
#         )
#         print("Crawled length:", len(result.cleaned_html))

#     # Multiple commands
#     js_commands = [
#         "window.scrollTo(0, document.body.scrollHeight);",
#         # 'More' link on Hacker News
#         "document.querySelector('a.morelink')?.click();",  
#     ]
#     config = CrawlerRunConfig(js_code=js_commands)

#     async with AsyncWebCrawler() as crawler:
#         result = await crawler.arun(
#             url="https://news.ycombinator.com",  # Another pass
#             config=config
#         )
#         print("After scroll+click, length:", len(result.cleaned_html))

# if __name__ == "__main__":
#     asyncio.run(main())
