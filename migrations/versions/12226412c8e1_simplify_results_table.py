"""simplify results table

Revision ID: 12226412c8e1
Revises: 0d19975bf2b2
Create Date: 2026-06-17 13:32:44.489107

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12226412c8e1'
down_revision = '0d19975bf2b2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.drop_column('first')
        batch_op.drop_column('second')
        batch_op.drop_column('third')
        batch_op.drop_column('fourth')
        batch_op.drop_column('fifth')
        batch_op.drop_column('sixth')
        batch_op.drop_column('seventh')
        batch_op.drop_column('eigth')
        batch_op.drop_column('ninth')
        batch_op.drop_column('tenth')
        batch_op.drop_column('eleventh')
        batch_op.drop_column('twelfth')
        batch_op.drop_column('thirtenth')
        batch_op.drop_column('fourtenth')
        batch_op.drop_column('fifthtenth')
        batch_op.drop_column('sixtenth')
        batch_op.drop_column('blood1')
        batch_op.drop_column('blood2')
        batch_op.drop_column('blood3')
        batch_op.drop_column('blood4')


def upgrade():
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.drop_column('first')
        batch_op.drop_column('second')
        batch_op.drop_column('third')
        batch_op.drop_column('fourth')
        batch_op.drop_column('fifth')
        batch_op.drop_column('sixth')
        batch_op.drop_column('seventh')
        batch_op.drop_column('eigth')
        batch_op.drop_column('ninth')
        batch_op.drop_column('tenth')
        batch_op.drop_column('eleventh')
        batch_op.drop_column('twelfth')
        batch_op.drop_column('thirtenth')
        batch_op.drop_column('fourtenth')
        batch_op.drop_column('fifthtenth')
        batch_op.drop_column('sixtenth')
        batch_op.drop_column('blood1')
        batch_op.drop_column('blood2')
        batch_op.drop_column('blood3')
        batch_op.drop_column('blood4')


def downgrade():
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blood4', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('blood3', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('blood2', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('blood1', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('sixtenth', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('fifthtenth', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('fourtenth', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('thirtenth', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('twelfth', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('eleventh', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('tenth', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('ninth', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('eigth', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('seventh', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('sixth', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('fifth', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('fourth', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('third', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('second', sa.String(length=255), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('first', sa.String(length=255), nullable=False, server_default=''))
