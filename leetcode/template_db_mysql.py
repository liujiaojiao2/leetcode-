"""
MySQL 数据库操作通用模板（Python）
复制此文件后，根据你的实际项目修改下方配置与示例代码。

依赖：
- 安装 PyMySQL：pip install pymysql

核心思想 / 模版要点：
- 使用上下文管理器统一管理连接、提交、回滚、关闭
- 将「执行查询」与「执行写操作」封装为通用函数
- 具体业务表再封装成 Repository / DAO 类
"""

import pymysql
from contextlib import contextmanager
from typing import Any, Iterable, List, Optional, Tuple


# ========== MySQL 连接配置 ==========
# 根据你自己的本地 / 远程 MySQL 环境修改
MYSQL_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "password",  # TODO: 修改为你的密码
    "database": "test_db",   # TODO: 修改为你的库名
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.Cursor,  # 如需字典结果可用 DictCursor
}


@contextmanager
def get_connection():
    """
    通用 MySQL 连接管理：
    - 进入时建立连接
    - 正常结束时自动 commit
    - 出现异常时自动 rollback 并抛出
    - 最后一定关闭连接
    """
    conn = pymysql.connect(**MYSQL_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_query(sql: str, params: Iterable[Any] = ()) -> List[Tuple[Any, ...]]:
    """
    执行 SELECT 查询，返回所有结果。

    模版用法：
        rows = execute_query(
            "SELECT id, name FROM users WHERE age > %s",
            (18,),
        )
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            rows = cursor.fetchall()
    return list(rows)


def execute_non_query(sql: str, params: Iterable[Any] = ()) -> int:
    """
    执行 INSERT / UPDATE / DELETE 等写操作，返回影响行数。

    模版用法：
        affected = execute_non_query(
            "UPDATE users SET name = %s WHERE id = %s",
            (new_name, user_id),
        )
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            return cursor.rowcount


# ========== 示例：单表操作封装成仓储类（Repository / DAO） ==========
class UserRepository:
    """
    示例：用户表的常见操作。
    实际使用时：
    - 修改表名 / 字段名
    - 按需扩展方法（分页查询、复杂筛选等）
    """

    def get_by_id(self, user_id: int) -> Optional[Tuple[Any, ...]]:
        sql = "SELECT id, name, age FROM users WHERE id = %s"
        rows = execute_query(sql, (user_id,))
        return rows[0] if rows else None

    def create(self, name: str, age: int) -> int:
        sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
        return execute_non_query(sql, (name, age))

    def update_name(self, user_id: int, new_name: str) -> int:
        sql = "UPDATE users SET name = %s WHERE id = %s"
        return execute_non_query(sql, (new_name, user_id))

    def delete(self, user_id: int) -> int:
        sql = "DELETE FROM users WHERE id = %s"
        return execute_non_query(sql, (user_id,))


# ========== 使用说明 ==========
"""
你需要准备的是：
1. MySQL 服务本身（本地或远程），可以通过：
   - 本地安装 MySQL Server
   - 或者使用 Docker 启动一个 MySQL 容器

2. 在 MySQL 中建好库和表，例如：

   CREATE DATABASE test_db DEFAULT CHARSET utf8mb4;

   USE test_db;

   CREATE TABLE IF NOT EXISTS users (
       id   INT PRIMARY KEY AUTO_INCREMENT,
       name VARCHAR(100) NOT NULL,
       age  INT NOT NULL
   );

3. 在本文件中修改 MYSQL_CONFIG 里的 user/password/database 等配置，
   与你实际的数据库一致。

然后你就可以在其他 Python 文件中：

    from template_db_mysql import UserRepository

    repo = UserRepository()
    repo.create("Alice", 20)
    user = repo.get_by_id(1)
    ...
"""


if __name__ == "__main__":
    # 简单自测（需要你已正确配置 MYSQL_CONFIG 并提前建好库 / 表）
    repo = UserRepository()
    print("当前 id=1 用户：", repo.get_by_id(1))

