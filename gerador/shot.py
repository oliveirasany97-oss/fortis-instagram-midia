import sys,asyncio
from playwright.async_api import async_playwright
async def m(src,out):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':1350})
        import os;await pg.goto('file://'+os.path.abspath(src));await pg.wait_for_timeout(600)
        await pg.screenshot(path=out);await b.close()
asyncio.run(m(sys.argv[1],sys.argv[2]))
