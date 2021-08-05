"""adding verified and attributes

Revision ID: 0b43b9043b64
Revises: 53a0362e1b51
Create Date: 2021-08-05 01:57:24.822133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0b43b9043b64"
down_revision = "53a0362e1b51"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "reviews", sa.Column("verified_purchase", sa.Boolean(), nullable=True)
    )
    op.add_column("reviews", sa.Column("attributes", sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("reviews", "attributes")
    op.drop_column("reviews", "verified_purchase")
    # ### end Alembic commands ###
