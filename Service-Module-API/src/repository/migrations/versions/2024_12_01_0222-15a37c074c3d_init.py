"""init

Revision ID: 15a37c074c3d
Revises: 
Create Date: 2024-12-01 02:22:41.342121

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '15a37c074c3d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('cin', sa.String(length=7), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('account_no', sa.String(length=12), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=12, scale=2), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cin')
    )
    op.create_index(op.f('ix_customers_account_no'), 'customers', ['account_no'], unique=False)
    op.create_table('function_job',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('function_name', sa.String(length=255), nullable=False),
    sa.Column('param_object', sa.String(length=255), nullable=False),
    sa.Column('param_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_function_job_customer_id'), 'function_job', ['customer_id'], unique=False)
    op.create_table('function_job_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('function_name', sa.String(length=255), nullable=False),
    sa.Column('param_object', sa.String(length=255), nullable=False),
    sa.Column('param_value', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_function_job_history_customer_id'), 'function_job_history', ['customer_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_function_job_history_customer_id'), table_name='function_job_history')
    op.drop_table('function_job_history')
    op.drop_index(op.f('ix_function_job_customer_id'), table_name='function_job')
    op.drop_table('function_job')
    op.drop_index(op.f('ix_customers_account_no'), table_name='customers')
    op.drop_table('customers')
    # ### end Alembic commands ###