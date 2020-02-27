from sqlalchemy import Table, Column, MetaData, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.sqltypes import String, Integer

metadata = MetaData()
# describes multiple tables(or databases) and keeps many different features
# of database

users = Table(
    'users',
    metadata,
    # schema='schema_name'
    # autoload=True for table reflection
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String)
)

# tables reflection - https://docs.sqlalchemy.org/en/14/core/reflection.html
# better read docs, if you need
# all tables can be reflected all at once

addresses = Table(
    'addresses',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('users.id', onupdate='CASCADE',
                                       ondelete='CASCADE')),
    # onupdate, ondelete may not be specified
    Column('email_address', String(50), nullable=False)
)

# primary_key - PK, nullable - NOT NULL, unique - UNIQUE
# default - Default Value, autoincrement: False, 'auto', ...

# for complexed foreign keys ForeignKeyConstraint is used like
# there are other constraints like PK, CHECK, UNIQUE
something = Table(
    'something',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email_address', String(50), nullable=False),
    Column('email_id', Integer, nullable=False),
    ForeignKeyConstraint(
        ('email_address', 'email_id'),
        ('addresses.email_address', 'addresses.id'),
        onupdate='CASCADE', ondelete='SET NULL')
)
