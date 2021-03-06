"""empty message

Revision ID: 412c6eb48725
Revises: 51b91ea44490
Create Date: 2016-11-17 09:41:09.832871

"""

# revision identifiers, used by Alembic.
revision = '412c6eb48725'
down_revision = '51b91ea44490'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('asker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asker_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_questions_timestamp', 'questions', ['timestamp'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_questions_timestamp', 'questions')
    op.drop_table('questions')
    ### end Alembic commands ###
