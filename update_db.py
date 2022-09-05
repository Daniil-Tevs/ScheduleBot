
def get_users_id(cur):
    try:
        cur.execute("SELECT user_id FROM public.user_data")

        users_id = list([i[0] for i in cur.fetchall()])
        return users_id

    except Exception:
        pass