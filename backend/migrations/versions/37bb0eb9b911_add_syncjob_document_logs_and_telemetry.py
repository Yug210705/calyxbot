"""Add SyncJob Document logs and telemetry

Revision ID: 37bb0eb9b911
Revises: 8b226c73c6a1
Create Date: 2026-07-04 00:50:42.598644

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37bb0eb9b911'
down_revision: str | Sequence[str] | None = '8b226c73c6a1'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Update SyncJobStatus Enum safely
    op.execute("ALTER TYPE syncjobstatus ADD VALUE IF NOT EXISTS 'CANCELLING'")
    op.execute("ALTER TYPE syncjobstatus ADD VALUE IF NOT EXISTS 'CANCELLED'")

    # Create sync_job_document_logs table
    op.create_table(
        'sync_job_document_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('sync_job_id', sa.UUID(), nullable=False),
        sa.Column('integration_id', sa.UUID(), nullable=False),
        sa.Column('document_id', sa.UUID(), nullable=True),
        sa.Column('external_document_id', sa.String(), nullable=True),
        sa.Column('document_title', sa.String(), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('outcome', sa.Enum('DISCOVERED', 'UNCHANGED', 'UPDATED', 'CREATED', 'DELETED', 'SKIPPED', 'FAILED', name='syncjobdocumentoutcome'), nullable=False),
        sa.Column('failure_reason_code', sa.String(), nullable=True),
        sa.Column('failure_message', sa.String(), nullable=True),
        sa.Column('bytes_processed', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('document_version_before', sa.Integer(), nullable=True),
        sa.Column('document_version_after', sa.Integer(), nullable=True),
        sa.Column('checksum_before', sa.String(), nullable=True),
        sa.Column('checksum_after', sa.String(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_ms', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('metadata_json', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
        sa.ForeignKeyConstraint(['integration_id'], ['connectors.id'], ),
        sa.ForeignKeyConstraint(['sync_job_id'], ['sync_jobs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sync_job_document_logs_external_document_id'), 'sync_job_document_logs', ['external_document_id'], unique=False)
    op.create_index(op.f('ix_sync_job_document_logs_sync_job_id'), 'sync_job_document_logs', ['sync_job_id'], unique=False)

    # Add columns to sync_jobs
    op.add_column('sync_jobs', sa.Column('documents_unchanged', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('sync_jobs', sa.Column('documents_deleted', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('sync_jobs', sa.Column('failure_reason_code', sa.String(), nullable=True))
    op.add_column('sync_jobs', sa.Column('provider_cursor_before', sa.String(), nullable=True))
    op.add_column('sync_jobs', sa.Column('provider_cursor_after', sa.String(), nullable=True))
    op.add_column('sync_jobs', sa.Column('parent_job_id', sa.UUID(), nullable=True))
    op.add_column('sync_jobs', sa.Column('cancel_requested_at', sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(None, 'sync_jobs', 'sync_jobs', ['parent_job_id'], ['id'])


def downgrade() -> None:
    # Remove columns from sync_jobs
    op.drop_constraint(None, 'sync_jobs', type_='foreignkey')
    op.drop_column('sync_jobs', 'cancel_requested_at')
    op.drop_column('sync_jobs', 'parent_job_id')
    op.drop_column('sync_jobs', 'provider_cursor_after')
    op.drop_column('sync_jobs', 'provider_cursor_before')
    op.drop_column('sync_jobs', 'failure_reason_code')
    op.drop_column('sync_jobs', 'documents_deleted')
    op.drop_column('sync_jobs', 'documents_unchanged')

    # Drop sync_job_document_logs table
    op.drop_index(op.f('ix_sync_job_document_logs_sync_job_id'), table_name='sync_job_document_logs')
    op.drop_index(op.f('ix_sync_job_document_logs_external_document_id'), table_name='sync_job_document_logs')
    op.drop_table('sync_job_document_logs')
    
    op.execute("DROP TYPE syncjobdocumentoutcome")
