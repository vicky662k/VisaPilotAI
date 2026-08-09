from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.services.application_data_service import (
    get_application_data,
)
from app.services.application_automation_service import (
    ApplicationAutomationService,
)


def run_application_workflow(
    db: Session,
    application_id: int,
    test_url: str | None = None,
) -> dict[str, Any]:

    data = get_application_data(
        db=db,
        application_id=application_id,
    )

    if not data:
        return {
            "success": False,
            "application_id": application_id,
            "error": "Application not found",
        }

    candidate = data["candidate"]

    field_values = {
        "#first_name": candidate["first_name"],
        "#last_name": candidate["last_name"],
        "#email": candidate["email"],
        "#phone": candidate["phone"],
        "#current_title": candidate["current_title"],
    }

    application_url = (
        test_url
        or data["application"]["application_url"]
    )

    if not application_url:
        return {
            "success": False,
            "application_id": application_id,
            "error": "Application URL not available",
        }

    automation = (
        ApplicationAutomationService()
        .start()
    )

    try:
        opened = automation.open_application(
            application_url
        )

        inspected = automation.inspect_page()

        filled = automation.fill_fields(
            field_values
        )

        validation = automation.validate_fields(
            list(field_values.keys())
        )

        return {
            "success": validation["valid"],
            "application_id": application_id,
            "open": opened,
            "inspect": inspected,
            "fill": filled,
            "validation": validation,
            "submitted": False,
        }

    finally:
        automation.close()