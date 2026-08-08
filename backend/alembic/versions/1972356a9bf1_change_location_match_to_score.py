"""Change location match to score

Revision ID: 1972356a9bf1
Revises: 35d655612b8a
Create Date: 2026-08-08 21:29:17.066748

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "1972356a9bf1"
down_revision: Union[str, Sequence[str], None] = "35d655612b8a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.alter_column(
        "job_matches",
        "location_match",
        existing_type=sa.BOOLEAN(),
        type_=sa.Float(),
        existing_nullable=False,
        postgresql_using="""
            CASE
                WHEN location_match = TRUE THEN 100.0
                ELSE 0.0
            END
        """,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "job_matches",
        "location_match",
        existing_type=sa.Float(),
        type_=sa.BOOLEAN(),
        existing_nullable=False,
        postgresql_using="""
            CASE
                WHEN location_match >= 50.0 THEN TRUE
                ELSE FALSE
            END
        """,
    )