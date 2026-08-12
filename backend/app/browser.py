from pathlib import Path

from playwright.async_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)


# SCREENSHOTS_DIR = Path("data/screenshots")
# PAGES_DIR = Path("data/pages")

async def capture_page(url: str) -> bytes:
    # SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    # PAGES_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        page = await browser.new_page(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1, # this gives us a predictable relationship between CSS pixels and screenshot pixels
        )

        try:
            await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=30_000,
            )

            await page.wait_for_load_state(
                "load",
                timeout=30_000,
            )

            await page.wait_for_timeout(2_000)

            try:
                screenshot =  await page.screenshot(
                    # path=SCREENSHOTS_DIR / "page.png",
                    full_page=True,
                    type="png",
                    animations="disabled",
                )

            except PlaywrightTimeoutError as error:
                raise RuntimeError(
                    "The screenshot operation timed out."
                ) from error
            
            except PlaywrightError as error:
                raise RuntimeError(
                    f"Failed to capture the website screenshot: {error}"
                ) from error
            
            return screenshot

                # print(f"Screenshot size: {len(screenshot)} bytes")

                # html = await page.content()

                # (PAGES_DIR / "page.html").write_text(
                #     html,
                #     encoding="utf-8"
                # )

                # print(f"Successfully captured: {url}")
                # print(f"Screenshot: {SCREENSHOTS_DIR / 'page.png'}")
                # print(f"HTML: {PAGES_DIR / 'page.html'}")
        
        except PlaywrightTimeoutError as error:
            raise RuntimeError(
                "The website took too long to read."
            ) from error

        except Exception as error:
            raise RuntimeError(
                f"Playwright failed to load the website: {error}"
            ) from error

        finally:
            await browser.close()