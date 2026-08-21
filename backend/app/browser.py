import base64
from pathlib import Path

from playwright.async_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    async_playwright,
)


SCREENSHOTS_DIR = Path("data/screenshots")


async def capture_page(url: str) -> dict:

    SCREENSHOTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()

        page = await browser.new_page(
            viewport={
                "width": 1440,
                "height": 900
            },
            device_scale_factor=1,
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

            await page.wait_for_timeout(
                2_000
            )


            try:
                screenshot_path = (
                    SCREENSHOTS_DIR / "page.png"
                )

                screenshot = await page.screenshot(
                    path=screenshot_path,
                    full_page=True,
                    type="png",
                    animations="disabled",
                )


                html = await page.content()


                elements = await page.evaluate(
                    """
                    () => {
                        const tags = [
                            "h1",
                            "h2",
                            "button",
                            "a",
                            "img",
                            "input",
                            "nav"
                        ];

                        return tags.flatMap(tag =>
                            Array.from(
                                document.querySelectorAll(tag)
                            )
                            .map(element => {

                                const rect =
                                    element.getBoundingClientRect();

                                return {
                                    tag:
                                        element.tagName
                                        .toLowerCase(),

                                    text:
                                        element.innerText
                                        || "",

                                    x: rect.x,
                                    y: rect.y,
                                    width: rect.width,
                                    height: rect.height
                                };
                            })
                        );
                    }
                    """
                )


            except PlaywrightTimeoutError as error:
                raise RuntimeError(
                    "The screenshot operation timed out."
                ) from error


            except PlaywrightError as error:
                raise RuntimeError(
                    f"Failed to capture the website screenshot: {error}"
                ) from error



            return {
                "screenshot": base64.b64encode(
                    screenshot
                ).decode("utf-8"),

                "screenshot_path": str(
                    screenshot_path
                ),

                "html": html,

                "elements": elements,
            }


        except PlaywrightTimeoutError as error:
            raise RuntimeError(
                "The website took too long to load."
            ) from error


        except Exception as error:
            raise RuntimeError(
                f"Playwright failed to load the website: {error}"
            ) from error


        finally:
            await browser.close()