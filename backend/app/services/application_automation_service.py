from typing import Any

from playwright.sync_api import (
    Browser,
    Page,
    sync_playwright,
)


class ApplicationAutomationService:
    """
    Controlled browser automation.

    Current scope:
    OPEN → INSPECT → MAP → FILL → VALIDATE

    Final submission is intentionally not performed.
    """

    def __init__(self):
        self.playwright = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=True
        )

        self.page = self.browser.new_page()

        return self

    def open_application(
        self,
        application_url: str,
    ) -> dict[str, Any]:

        if not self.page:
            raise RuntimeError(
                "Automation browser is not started"
            )

        response = self.page.goto(
            application_url,
            wait_until="domcontentloaded",
        )

        return {
            "url": self.page.url,
            "title": self.page.title(),
            "status_code": (
                response.status
                if response
                else None
            ),
        }

    def inspect_page(self) -> dict[str, Any]:

        if not self.page:
            raise RuntimeError(
                "Automation browser is not started"
            )

        inputs = self.page.locator(
            "input, textarea, select"
        )

        fields = []

        for index in range(inputs.count()):
            element = inputs.nth(index)

            fields.append(
                {
                    "index": index,
                    "tag": element.evaluate(
                        "(el) => el.tagName"
                    ),
                    "type": element.get_attribute(
                        "type"
                    ),
                    "name": element.get_attribute(
                        "name"
                    ),
                    "id": element.get_attribute(
                        "id"
                    ),
                    "placeholder": (
                        element.get_attribute(
                            "placeholder"
                        )
                    ),
                    "aria_label": (
                        element.get_attribute(
                            "aria-label"
                        )
                    ),
                }
            )

        return {
            "url": self.page.url,
            "title": self.page.title(),
            "fields": fields,
        }

    def fill_fields(
        self,
        field_values: dict[str, str],
    ) -> dict[str, Any]:

        if not self.page:
            raise RuntimeError(
                "Automation browser is not started"
            )

        filled = []

        for selector, value in field_values.items():

            element = self.page.locator(
                selector
            ).first

            if element.count() == 0:
                continue

            element.fill(str(value))

            filled.append(
                {
                    "selector": selector,
                    "filled": True,
                }
            )

        return {
            "filled_fields": filled,
            "count": len(filled),
        }

    def validate_fields(
        self,
        selectors: list[str],
    ) -> dict[str, Any]:

        if not self.page:
            raise RuntimeError(
                "Automation browser is not started"
            )

        results = []

        for selector in selectors:

            element = self.page.locator(
                selector
            ).first

            exists = element.count() > 0

            value = None

            if exists:
                value = element.input_value()

            results.append(
                {
                    "selector": selector,
                    "exists": exists,
                    "value": value,
                }
            )

        return {
            "valid": all(
                item["exists"]
                for item in results
            ),
            "fields": results,
        }

    def close(self):

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

        self.browser = None
        self.page = None
        self.playwright = None