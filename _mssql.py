from os import getenv
from dotenv import load_dotenv
from mssql_python import connect

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取连接字符串并建立数据库连接
conn = connect(getenv("SQL_CONNECTION_STRING"))

try:
    cursor = conn.cursor()

    cursor.execute("select @@VERSION as version_info")

    rows = cursor.fetchall()
    for row in rows:
        print(f"连接成功，数据库版本信息：{row.version_info}")
except Exception as e:
    print(f"连接或查询失败：{e}")
finally:
    if conn:
        conn.close()
