"""empty message

Revision ID: d51b6d50a14d
Revises: None
Create Date: 2017-04-07 21:17:41.623672

"""

# revision identifiers, used by Alembic.
revision = 'd51b6d50a14d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('branches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('semester', sa.Integer(), nullable=True),
    sa.Column('Date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('elections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('branch', sa.String(length=64), nullable=True),
    sa.Column('sid', sa.BigInteger(), nullable=True),
    sa.Column('sem', sa.Integer(), nullable=True),
    sa.Column('votes', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('sid')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('has_voted', sa.Boolean(), nullable=True),
    sa.Column('s_no', sa.BigInteger(), nullable=True),
    sa.Column('branch', sa.String(), nullable=True),
    sa.Column('semester', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_s_no'), 'users', ['s_no'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_s_no'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('elections')
    op.drop_table('branches')
    # ### end Alembic commands ###