"""Initial migration

Revision ID: 001
Create Date: 2024-02-20

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

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
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('device_type', sa.Integer(), nullable=True),
        sa.Column('location_type', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_active', sa.DateTime(), nullable=True),
        sa.Column('preferences', sqlite.JSON, nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index('ix_users_username', 'users', ['username'])

    # Create videos table
    op.create_table(
        'videos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('external_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('video_metadata', sqlite.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('external_id')
    )
    op.create_index('ix_videos_external_id', 'videos', ['external_id'])
    op.create_index('ix_videos_category', 'videos', ['category'])

    # Create user_interactions table
    op.create_table(
        'user_interactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('video_id', sa.Integer(), nullable=False),
        sa.Column('interaction_type', sa.String(), nullable=False),
        sa.Column('value', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('context', sqlite.JSON, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['video_id'], ['videos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create recommendation_cache table
    op.create_table(
        'recommendation_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('recommendations', sqlite.JSON, nullable=True),
        sa.Column('context', sqlite.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_valid', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create mood_based_cache table
    op.create_table(
        'mood_based_cache',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('mood', sa.String(), nullable=False),
        sa.Column('recommendations', sqlite.JSON, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('is_valid', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_mood_based_cache_mood', 'mood_based_cache', ['mood'])

def downgrade() -> None:
    op.drop_table('mood_based_cache')
    op.drop_table('recommendation_cache')
    op.drop_table('user_interactions')
    op.drop_table('videos')
    op.drop_table('users') 