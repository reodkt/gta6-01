import asyncio, sys
from playwright.async_api import async_playwright

SHOTS = [
    ("1-play", "?shot=play&seed=1"),
    ("2-heat", "?shot=heat&seed=1"),
    ("3-late", "?shot=late&seed=1"),
    ("4-end", "?shot=end&seed=1"),
]

async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        for name, q in SHOTS:
            await page.goto("http://localhost:8123/index.html" + q)
            await page.wait_for_selector("canvas#__ready", state="attached", timeout=30000)
            await page.screenshot(path=f"/tmp/makefun/gta6-repo/screenshots/{name}.jpg", quality=88, type="jpeg")
            print("shot", name, "done")
        await browser.close()
        if errors:
            print("PAGE ERRORS:", *errors[:10], sep="\n")

asyncio.run(main())
