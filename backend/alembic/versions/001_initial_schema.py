"""Initial schema - Users and MissionLogs tables

Revision ID: 001
Revises: 
Create Date: 2026-05-12 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=128), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create mission_logs table
    op.create_table(
        'mission_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('command', sa.String(length=255), nullable=False),
        sa.Column('response', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_mission_logs_id'), 'mission_logs', ['id'], unique=False)
    op.create_index(op.f('ix_mission_logs_username'), 'mission_logs', ['username'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_mission_logs_username'), table_name='mission_logs')
    op.drop_index(op.f('ix_mission_logs_id'), table_name='mission_logs')
    op.drop_table('mission_logs')

    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
