from pathlib import Path

from app.database.database import SessionLocal
from app.services.application_data_service import (
    get_application_data,
)
from app.services.application_automation_service import (
    ApplicationAutomationService,
)


db = SessionLocal()

try:
    application_id = 1

    data = get_application_data(
        db=db,
        application_id=application_id,
    )

    if not data:
        raise RuntimeError(
            "Application not found"
        )

    candidate = data["candidate"]

    field_values = {
        "#first_name": candidate["first_name"],
        "#last_name": candidate["last_name"],
        "#email": candidate["email"],
        "#phone": candidate["phone"],
        "#current_title": candidate["current_title"],
    }

    test_form = (
        Path("test_application_form.html")
        .resolve()
        .as_uri()
    )

    automation = (
        ApplicationAutomationService()
        .start()
    )

    try:
        opened = automation.open_application(
            test_form
        )

        print("OPEN:")
        print(opened)

        inspected = automation.inspect_page()

        print("INSPECT:")
        print(inspected)

        filled = automation.fill_fields(
            field_values
        )

        print("FILL:")
        print(filled)

        validation = automation.validate_fields(
            list(field_values.keys())
        )

        print("VALIDATE:")
        print(validation)

    finally:
        automation.close()

finally:
    db.close()