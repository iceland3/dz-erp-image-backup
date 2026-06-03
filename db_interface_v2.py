import os
from contextlib import contextmanager
from dotenv import load_dotenv
from mssql_python import connect

load_dotenv()

@contextmanager
def get_db_connection():
    """
    数据库连接上下文管理器
    使用 with 语句时，会自动处理连接的建立和关闭
    """
    conn_str = os.getenv("SQL_CONNECTION_STRING")
    assert conn_str is not None, "SQL_CONNECTION_STRING environment variable not set."
    conn = connect(conn_str)
    try:
        yield conn  # 交出连接对象供外部使用
    except Exception as e:
        conn.rollback() # 如果发生异常，回滚事务
        print(f"数据库事务异常：{e}")
        raise
    finally:
        conn.close() # 无论如何，最终都会关闭连接

def execute_query(sql, params=None):
    """
    封装好的查询接口
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()