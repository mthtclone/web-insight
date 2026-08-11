from pathlib import Path

from playwright.async_api import async_playwright

SCREENSHOTS_DIR = Path("data/screenshots")
PAGES_DIR = Path("data/pages")

async def capture_page(url: str) -> bytes:
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        page = await browser.new_page(
            viewport={"width": 1440, "height": 900}
        )

        try:
            await page.goto(
                url,
                wait_until="networkidle",
                timeout=30_000,
            )

            screenshot =  await page.screenshot(
                path=SCREENSHOTS_DIR / "page.png",
                full_page=True,
            )

            # html = await page.content()

            # (PAGES_DIR / "page.html").write_text(
            #     html,
            #     encoding="utf-8"
            # )

            # print(f"Successfully captured: {url}")
            # print(f"Screenshot: {SCREENSHOTS_DIR / 'page.png'}")
            # print(f"HTML: {PAGES_DIR / 'page.html'}")

            return screenshot

        except Exception as error:
            print(f"Failed to capture {url}")
            print(f"Error: {error}")

        finally:
            await browser.close()