import psycopg2

con = psycopg2.connect(
    database="da9ueqg4mqu8o1",
    user="rtijlvzrnnclrb",
    password="235899f24fffb504c10520411c96c7210782308ed71de37bfeed638043414ef4",
    host="ec2-99-81-16-126.eu-west-1.compute.amazonaws.com",
    port="5432"
)


def make_user(id, id_group):
    global con
    try:
        with con.cursor() as cur:
            cur.execute(
                "INSERT INTO user_data(user_id, id_group) VALUES ('{}', '{}')".format(str(id), str(id_group))
            )
            con.commit()
    except Exception:
        pass


def get_users_id():
    global con
    try:
        with con.cursor() as cur:
            cur.execute('SELECT user_id FROM user_data')
            con.commit()

            users_id = list([i[0] for i in cur.fetchall()])
            return users_id

    except Exception:
        pass


def get_group(user_id):
    global con
    try:
        with con.cursor() as cur:
            cur.execute("SELECT id_group FROM user_data WHERE user_id='{}'".format(str(user_id)))
            tmp = cur.fetchall()
            if tmp:
                group = tmp[0][0]
                con.commit()
                return group
            else:
                con.commit()
                return " "
    except Exception:
        pass


def delete_user(user_id):
    global con
    try:
        with con.cursor() as cur:
            cur.execute("DELETE FROM user_data WHERE user_id='{}'".format(str(user_id)))
            con.commit()
    except Exception:
        pass
