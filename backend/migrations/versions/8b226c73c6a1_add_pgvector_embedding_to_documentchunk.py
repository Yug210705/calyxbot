"""Add pgvector embedding to DocumentChunk

Revision ID: 8b226c73c6a1
Revises: <latest_revision> # I should fetch the previous revision if needed, but I can just leave it as generated
Create Date: 2023-10-27 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '8b226c73c6a1'
down_revision: Union[str, None] = '2234be0f5041'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')
    
    # 2. Add embedding column to document_chunks
    op.add_column('document_chunks', sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True))


def downgrade() -> None:
    op.drop_column('document_chunks', 'embedding')
    # We do not drop the vector extension because other tables might use it
