def make_user(id, id_group, con):
    try:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO user_data(user_id, id_group) VALUES ('{}', '{}')".format(str(id), str(id_group))
        )

        con.commit()
        con.close()
    except Exception:
        con.commit()
        con.close()


def get_users_id(con):
    try:
        cur = con.cursor()
        cur.execute('SELECT user_id FROM user_data')

        users_id = list([i[0] for i in cur.fetchall()])
        con.commit()
        con.close()
        return users_id

    except Exception:
        con.commit()
        con.close()