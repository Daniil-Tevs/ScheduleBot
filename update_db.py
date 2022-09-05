
import psycopg2
con = psycopg2.connect(
    database="da9ueqg4mqu8o1",
    user="rtijlvzrnnclrb",
    password="235899f24fffb504c10520411c96c7210782308ed71de37bfeed638043414ef4",
    host="ec2-99-81-16-126.eu-west-1.compute.amazonaws.com",
    port="5432"
)

def make_user(id, id_group):
    try:
        global con
        cur = con.cursor()
        cur.execute(
            "INSERT INTO user_data(user_id, id_group) VALUES ('{}', '{}')".format(str(id), str(id_group))
        )

        con.commit()
    except Exception:
        con.commit()


def get_users_id():
    try:
        global con
        cur = con.cursor()
        cur.execute("SELECT user_id FROM user_data")

        users_id = list([i[0] for i in cur.fetchall()])
        con.commit()
        return users_id

    except Exception:
        con.commit()