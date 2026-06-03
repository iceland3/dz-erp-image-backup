from os import getenv
from dotenv import load_dotenv
from mssql_python import connect

# 加载 .env 文件中的环境变量
load_dotenv()

def execute_query(sql, params=None):
    """
    通用的数据库查询接口
    :param sql: 要执行的 SQL 语句
    :param params: SQL 语句的参数（可选，防止SQL注入）
    :return: 查询结果的列表
    """
    conn = None
    try:
        # 每次调用时建立连接
        conn_str = getenv("SQL_CONNECTION_STRING")
        assert conn_str is not None, "缺少 SQL_CONNECTION_STRING 环境变量"
        conn = connect(conn_str)
        cursor = conn.cursor()

        # 执行SQL语句
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        # 获取所有结果
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print(f"数据库操作失败：{e}")
        return []
    finally:
        # 确保连接被关闭
        if conn:
            conn.close()