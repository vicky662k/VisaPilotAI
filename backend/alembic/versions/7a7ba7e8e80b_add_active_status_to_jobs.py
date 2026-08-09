"""Add active status to jobs

Revision ID: 7a7ba7e8e80b
Revises: 1972356a9bf1
Create Date: 2026-08-09
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a7ba7e8e80b"
down_revision: Union[str, Sequence[str], None] = "1972356a9bf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "jobs",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
            server_default=sa.true(),
        ),
    )

    op.execute(
        "UPDATE jobs SET is_active = TRUE WHERE is_active IS NULL"
    )

    op.alter_column(
        "jobs",
        "is_active",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.true(),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "jobs",
        "is_active",
    )