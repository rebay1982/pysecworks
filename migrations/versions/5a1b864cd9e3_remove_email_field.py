"""remove email field

Revision ID: 5a1b864cd9e3
Revises: d311bdecd13a
Create Date: 2022-02-05 09:44:58.559698

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a1b864cd9e3'
down_revision = 'd311bdecd13a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.VARCHAR(length=120), nullable=True))
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    # ### end Alembic commands ###
