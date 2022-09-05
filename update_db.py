def make_user(id, id_group, cur,con):
    try:
        cur.execute(
            "INSERT INTO public.user_data(user_id, id_group) VALUES ('{}', '{}')".format(str(id), str(id_group))
        )
        con.commit()
    except Exception:
        pass


def get_users_id(cur):
    try:
        cur.execute("SELECT user_id FROM public.user_data")

        users_id = list([i[0] for i in cur.fetchall()])
        return users_id

    except Exception:
        pass