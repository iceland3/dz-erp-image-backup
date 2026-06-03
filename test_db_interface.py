from db_interface_v2 import get_db_connection

sql = "INSERT INTO image_backup (billid, tableid, billstate, image) VALUES (100, 1, 2, 'test.jpg');"

with get_db_connection() as conn:
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        conn.commit()

        cursor.execute("select scope_identity()")
        new_id_row = cursor.fetchone()
        if new_id_row:
            print(f"插入成功，新纪录的id是 {new_id_row[0]}")
        else:
            print("插入成功，但未获取到 id")

    except Exception as e:
        conn.rollback()
        print(f"发生错误：{e}")