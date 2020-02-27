from sqlalchemy.sql.dml import Insert, Update, Delete
from sqlalchemy.sql.expression import select, and_, or_, not_, text, func, \
    bindparam
# all elements, functions etc. here
# https://docs.sqlalchemy.org/en/14/core/expression_api.html

from src.tables import users, addresses


def insert_users(id=None, name='Jack', fullname='Jack Jones', empty=False) -> \
        Insert:
    # users.insert(...)
    if empty:
        return users.insert()

    return users.insert(values={'id': id, 'name': name, 'fullname': fullname})


def insert_address() -> Insert:
    # addresses.insert(...)
    return addresses.insert()


def select_users():
    # users.select(...)
    return select([users])


def select_addresses(columns=None):
    selection = []

    if columns:
        for column in columns:
            selection.append(getattr(addresses.c, column))
            # e.g. addresses.c.email or addresses.columns.email
    else:
        selection.append(addresses)

    return select(selection)


# selections may contain several tables like select([users.c.name, addresses])
# using where with select is possible
# select([addresses, users]).where(users.c.id == addresses.c.user_id)


def complicated_select():
    return select(
        [
            addresses,
            users.c.id,
            (users.c.name + ', ' + users.c.fullname).label('title')
        ]
    ).where(
        and_(
            users.c.id == addresses.c.user_id,
            or_(
                addresses.c.email_address.like('%@www.org'),
                addresses.c.email_address.like(bindparam('email_address'))
                # Attention to bindparam. It is taken from con.execute directly
            )
        )
    )


def textual_sql(query: str = ''):
    # better to read docs there.
    # https://docs.sqlalchemy.org/en/14/core/tutorial.html#using-textual-sql
    return text(query)


def using_functions():
    return select([
        addresses.c.user_id,
        func.count(addresses.c.id).label('num_addresses')
    ]) \
        .group_by('user_id') \
        .order_by('user_id')


def using_join():
    return select([users.c.fullname]).select_from(
        users.join(addresses)  # clause can be used like
        # addresses.c.email_address.like(users.c.name + '%')
    )
