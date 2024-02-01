"""empty message

Revision ID: 820f19d4fb3b
Revises: 
Create Date: 2024-01-28 19:34:18.132952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '820f19d4fb3b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('failed_login_attempts',
    sa.Column('log_id', sa.Integer(), nullable=False),
    sa.Column('log_uuid', sa.String(length=256), nullable=True),
    sa.Column('ip_address', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('log_id')
    )
    with op.batch_alter_table('failed_login_attempts', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_failed_login_attempts_log_uuid'), ['log_uuid'], unique=False)

    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_uuid', sa.String(length=256), nullable=True),
    sa.Column('forename', sa.String(length=256), nullable=True),
    sa.Column('lastname', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('phone_number', sa.String(length=256), nullable=True),
    sa.Column('is_verified', sa.Boolean(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    with op.batch_alter_table('failed_login_attempts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_failed_login_attempts_log_uuid'))

    op.drop_table('failed_login_attempts')
    # ### end Alembic commands ###