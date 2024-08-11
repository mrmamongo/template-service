"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""
import os

import sqlalchemy as sa
from alembic import context
from alembic import op
from dotenv import load_dotenv
from loguru import logger

from src.config import get_config
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

cfg = get_config()

def upgrade():
    % for schema in enabled_pg_schemas:
    op.execute('CREATE SCHEMA IF NOT EXISTS ${schema}')
    % endfor

    schema_upgrades()
    # x-flag for data
    if context.get_x_argument(as_dictionary=True).get("data", None):
        data_upgrades()

    logger.info("Migration complete [OK]")


def downgrade():
    data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here."""
    ${upgrades if upgrades else "pass"}

def schema_downgrades():
    """schema downgrade migrations go here."""
    ${downgrades if downgrades else "pass"}

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass

