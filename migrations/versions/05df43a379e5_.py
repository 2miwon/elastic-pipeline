"""empty message

Revision ID: 05df43a379e5
Revises: 
Create Date: 2024-02-04 14:55:01.248639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '05df43a379e5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bills',
    sa.Column('bill_no', sa.Integer(), nullable=False),
    sa.Column('bill_id', sa.String(255), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('file_link', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('bill_no')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('law',
    sa.Column('id', mysql.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('law_id', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('law_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('law_num', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('law_url', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('keyword',
    sa.Column('id', mysql.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('value', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('UK_9icifcsug0tr5q3qd5963kw1c', 'keyword', ['value'], unique=True)
    op.create_table('subscription',
    sa.Column('id', mysql.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('keyword_id', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['keyword_id'], ['keyword.id'], name='FKcecx8jcy1fg36gqo0a0stpxij'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='FK8l1goo02px4ye49xd7wgogxg6'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('user',
    sa.Column('id', mysql.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('picture', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('role', mysql.ENUM('GUEST', 'USER'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('email',
    sa.Column('id', mysql.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('message_body', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('sender', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('subject', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('receiver', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('receiver_id', mysql.BIGINT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['receiver'], ['user.id'], name='FKdeskct8ryqg6e84k4jxhtklmg'),
    sa.ForeignKeyConstraint(['receiver_id'], ['user.id'], name='FK2grayjdqerssrtf9rwsqy58d'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('bills')
    # ### end Alembic commands ###
