import sqlalchemy
from sqlalchemy import create_engine

from src.tables import metadata
from .crud import insert_users, insert_address, select_users, select_addresses, \
    complicated_select, using_functions, using_join


def main():
    # print(sqlalchemy.__version__)
    engine = create_engine(r'sqlite:///sqlite.db')  # echo=True for explicit log
    metadata.drop_all(engine)  # or users.drop(engine); addresses...
    metadata.create_all(engine)  # or users.create(engine); addresses...
    # access available tables via metadata.tables
    con = engine.connect()
    # transaction can be used here
    # trans = con.begin()
    # try:
    #     # your code
    #     trans.commit()
    # except:
    #     trans.rollback()

    # transaction may be created like
    # with engine.begin() as trans:

    con.execute(insert_users())
    res = con.execute(insert_users(empty=True), name='Aliaksei',
                      fullname='Aliaksei Prakapenka')
    print(res.inserted_primary_key)

    con.execute(insert_address(), [
        {'user_id': 1, 'email_address': 'jack@yahoo.com'},
        {'user_id': 1, 'email_address': 'jack@msn.com'},
        {'user_id': 2, 'email_address': 'www@www.org'}
    ])

    res: sqlalchemy.engine.result.ResultProxy = con.execute(select_users())
    print(res.fetchone())  # -> first element
    for row in res:  # -> start from second since uses fetchone()
        print(row['name'])
    print(res.fetchone())  # -> None
    res = con.execute(select_addresses(columns=['email_address', 'user_id']))
    for user_id, email in res:
        print(user_id, email)
    print(con.execute(complicated_select(), email_address='yahoo.com')
                     # Attention here, bindparam used for email_address
          .fetchall())
    print(con.execute(using_functions()).fetchall())
    print(con.execute(using_join()).fetchall())

    con.close()
