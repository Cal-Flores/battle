"""empty message

Revision ID: 9ed49bb30271
Revises: 438fba8814b5
Create Date: 2025-01-01 21:18:50.154667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ed49bb30271'
down_revision = '438fba8814b5'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns with default values
    op.add_column('results', sa.Column('eleventh', sa.String(length=255), nullable=True, server_default=''))
    op.add_column('results', sa.Column('twelfth', sa.String(length=255), nullable=True, server_default=''))

def downgrade():
    # Drop the columns if downgrading
    op.drop_column('results', 'twelfth')
    op.drop_column('results', 'eleventh')
