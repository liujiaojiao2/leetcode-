"""
数据库操作通用模板（Python）
复制此文件后，根据你的实际项目修改下方配置与示例代码。

适用场景：
- 小型脚本 / 工具：需要快速读写本地数据库（推荐 sqlite）
- 练习「数据库题」或封装 CRUD 逻辑时，作为通用骨架

核心思想 / 模版要点：
- 使用上下文管理器（context manager）统一管理连接、提交、回滚、关闭
- 将「执行查询」与「执行写操作」封装成两个通用函数
- 具体业务表（如 User）再封装成 Repository / DAO 类，只暴露清晰的方法名
"""

import sqlite3
from contextlib import contextmanager
from typing import Any, Iterable, List, Optional, Tuple


# ========== 数据库配置 ==========
# 默认使用本地 sqlite 数据库，根据需要自行修改路径或改成 MySQL / PostgreSQL 连接方式
DB_PATH = "example.db"  # TODO: 修改为你的数据库路径


@contextmanager
def get_connection(db_path: str = DB_PATH):
    """
    通用连接管理：
    - 进入时建立连接
    - 正常结束时自动 commit
    - 出现异常时自动 rollback 并抛出
    - 最后一定关闭连接
    """
    conn = sqlite3.connect(db_path)
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
    执行 SELECT 等查询语句，返回所有结果。

    模版用法：
        rows = execute_query("SELECT id, name FROM users WHERE age > ?", (18,))
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
    return rows


def execute_non_query(sql: str, params: Iterable[Any] = ()) -> int:
    """
    执行 INSERT / UPDATE / DELETE 等写操作，返回影响行数。

    模版用法：
        affected = execute_non_query(
            "UPDATE users SET name = ? WHERE id = ?",
            (new_name, user_id),
        )
    """
    with get_connection() as conn:
        cursor = conn.cursor()
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
        sql = "SELECT id, name, age FROM users WHERE id = ?"
        rows = execute_query(sql, (user_id,))
        return rows[0] if rows else None

    def create(self, name: str, age: int) -> int:
        sql = "INSERT INTO users (name, age) VALUES (?, ?)"
        return execute_non_query(sql, (name, age))

    def update_name(self, user_id: int, new_name: str) -> int:
        sql = "UPDATE users SET name = ? WHERE id = ?"
        return execute_non_query(sql, (new_name, user_id))

    def delete(self, user_id: int) -> int:
        sql = "DELETE FROM users WHERE id = ?"
        return execute_non_query(sql, (user_id,))


# ========== 本地测试 / 使用示例 ==========
if __name__ == "__main__":
    repo = UserRepository()

    # 初始化示例表（实际项目中可以单独弄建表脚本）
    execute_non_query(
        """
        CREATE TABLE IF NOT EXISTS users (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age  INTEGER NOT NULL
        )
        """
    )

    # 创建
    affected = repo.create("Alice", 20)
    print(f"Inserted rows: {affected}")

    # 查询
    user = repo.get_by_id(1)
    print("User #1:", user)

    # 更新
    repo.update_name(1, "Bob")
    print("After update:", repo.get_by_id(1))

    # 删除
    repo.delete(1)
    print("After delete:", repo.get_by_id(1))

