"""Added user_id and state to Log

Revision ID: a489c2ea5f42
Revises: 4c2b3deafee1
Create Date: 2019-09-06 17:05:07.396064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a489c2ea5f42'
down_revision = '4c2b3deafee1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('log', sa.Column('state', sa.String(length=255), nullable=True))
    op.add_column('log', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'log', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'log', type_='foreignkey')
    op.drop_column('log', 'user_id')
    op.drop_column('log', 'state')
    # ### end Alembic commands ###
