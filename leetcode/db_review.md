"""
数据库复习文档（LeetCode / 机试向）
后续可以在本文件中持续追加其它数据库题目的思路与知识点。
"""

## 总体使用说明

- 本文档主要面向 **字节跳动机试 / LeetCode 数据库题** 的快速复习。
- 建议每道题都按照统一模板记录：**题目 → 表结构 → 思路 → 解法 SQL → 知识点**。
- 在线做题（LeetCode / 牛客）时只需要写 SQL，本地不一定要真的运行 MySQL。

---

## 通用 JOIN 模板（记忆核心）

### 左连接（LEFT JOIN）通用写法

**场景**：以左表为主，右表是「补充信息」，右表没有记录时，对应列为 `NULL` 但左表行仍然保留。

```sql
SELECT
    l.列1,
    l.列2,
    r.列A,
    r.列B
FROM 左表 AS l
LEFT JOIN 右表 AS r
    ON l.键 = r.键;
```

- **LEFT JOIN 记忆**：左表全要，右表有则拼上，没有则 `NULL`。
- 常见题型：**用户 + 可能有的扩展信息**，例如「人 + 地址」「用户 + 邮箱」「订单 + 退款」等。

### 常见 JOIN 类型对比（考试够用版）

- **INNER JOIN**：两边都匹配上的才保留 → 交集。
- **LEFT JOIN**：左表全部保留，右表没有时为 `NULL`。
- **RIGHT JOIN**：右表全部保留，左表没有时为 `NULL`。

实际做题中：
- 题目说「即使没有某信息也要出现主记录」→ 往往是 `LEFT JOIN`。
- 题目只关心「两边都匹配的记录」→ 往往是 `INNER JOIN`。

---

## 题目模板（推荐每题按此结构整理）

建议每道数据库题在本文档中使用如下模板追加内容：

```text
### 题号 标题（如：175 组合两个表）

**表结构：**
- 表1：
  - 列名 / 含义 / 主键 / 外键等
- 表2：
  - 列名 / 含义 / 主键 / 外键等

**题目要求：**
- 用自然语言简要写清楚需要返回什么字段、什么条件。

**思路（人话版）：**
- 从哪张表出发（主表是谁）？
- 是否需要 JOIN，JOIN 条件是什么？
- 结果中哪些字段来自哪张表？
- 有没有「缺少记录时也要保留」这种需求（对应 LEFT JOIN）。

**标准解法 SQL：**
```sql
-- 在这里写最终 SQL
SELECT ...
FROM   ...
...
```

**知识点总结：**
- 涉及哪些 SQL 知识（如：LEFT JOIN / 聚合 / 分组 / 排序等）。
- 容易犯的错（比如误用 INNER JOIN 导致丢行、错写关联键等）。
```

---

## 示例：LeetCode 175. 组合两个表

**表结构：**

`Person`
```text
+----------+---------+
| PersonId | int     |  主键
| FirstName| varchar |
| LastName | varchar |
+----------+---------+
```

`Address`
```text
+----------+---------+
| AddressId| int     |  主键
| PersonId | int     |  外键，指向 Person.PersonId
| City     | varchar |
| State    | varchar |
+----------+---------+
```

**题目要求：**

输出每个人的 `FirstName, LastName, City, State`：
- 有地址则正常返回 `City, State`；
- 没有地址的人的 `City, State` 应为 `NULL`，人仍然要出现在结果中。

**思路（人话版）：**

- 题目是「以人（Person）为主」，地址如果有就拼上，没有也要把人列出来。
- 数学翻译：**以 Person 为主表，LEFT JOIN Address**。
- 关联字段是 `Person.PersonId = Address.PersonId`。
- SELECT 时按题目指定字段和顺序输出。

**标准解法 SQL：**

```sql
SELECT
    p.FirstName,
    p.LastName,
    a.City,
    a.State
FROM Person AS p
LEFT JOIN Address AS a
    ON p.PersonId = a.PersonId;
```

**本题知识点总结：**

- **LEFT JOIN 使用：**
  - 当题目要求「主表记录必须全部出现，即使右表没有匹配记录」时，使用 `LEFT JOIN`。
  - 本题中：主表是 `Person`，右表是 `Address`。
- **NULL 的来源：**
  - `LEFT JOIN` 时，若右表无匹配行，其列（如 `City`, `State`）自动为 `NULL`。
- **为什么不用 INNER JOIN：**
  - `INNER JOIN` 只保留两边都匹配的行，没有地址的人会被过滤掉，与题目要求冲突。
- **别名（AS）习惯：**
  - `Person AS p`, `Address AS a` 让 SQL 更短、更清晰，机试时推荐始终使用别名。

---

## 示例：LeetCode 181. 超过经理收入的员工

**表结构：**

`Employee`
```text
+----------+---------+
| Id       | int     |  主键
| Name     | varchar |
| Salary   | int     |
| ManagerId| int     |  外键，指向 Employee.Id（经理）
+----------+---------+
```

**题目要求：**

返回所有「工资严格高于自己经理工资」的员工名字，列名为 `Employee`。

**思路（人话版）：**

- 员工和经理都在同一张表内，需要 **自连接（self join）**。
- 给员工表起别名 `e`，经理表起别名 `m`：
  - 连接条件：`e.ManagerId = m.Id`。
- 在筛选条件中比较工资：`e.Salary > m.Salary`。
- 最后 `SELECT e.Name AS Employee` 按题目要求输出列名。

**标准解法 SQL：**

```sql
SELECT
    e.Name AS Employee
FROM Employee AS e
JOIN Employee AS m
    ON e.ManagerId = m.Id
WHERE e.Salary > m.Salary;
```

**本题知识点总结：**

- **自连接（self join）：**
  - 当一张表的某列引用本表的另一行（如 ManagerId → Id）时，用同一张表两次，起不同别名。
  - 典型形式：`FROM T AS a JOIN T AS b ON a.键 = b.键或主键`。
- **比较同表两行字段：**
  - 自连接后可以在 `WHERE` 中做 `a.col > b.col` 之类的比较。
- **INNER JOIN 选择：**
  - 只关心「有经理且工资高于经理」的员工，没经理的不需要出现在结果中，因此使用 `INNER JOIN` 即可。
- **别名语义清晰：**
  - `e` 代表 employee（员工），`m` 代表 manager（经理），阅读 SQL 时一眼能看懂角色。

**自连接通用模版（同表比较用）：**

```sql
SELECT
    a.需要的字段
FROM 表名 AS a
JOIN 表名 AS b
    ON a.关联字段 = b.关联字段或主键
WHERE
    a.字段 与 b.字段 做比较（如 a.col > b.col、a.col = b.col 等）;
```

---

## 示例：LeetCode 176. 第二高的薪水

**表结构：**

`Employee`
```text
+----------+---------+
| Id       | int     |  主键
| Salary   | int     |
+----------+---------+
```

**题目要求：**

返回表中「第二高的不同工资」，列名为 `SecondHighestSalary`：

- 若存在至少两个不同的工资 → 返回第二高的那个；
- 若不存在（只有 0 或 1 个不同工资）→ 返回 `NULL`。

**思路（人话版）：**

- 本质是从所有 **不同的工资** 中，取第 2 高。
- 常用两种思路：
  1. 去重后按工资从大到小排序，用 `LIMIT 1 OFFSET 1` 取第 2 条；
  2. 先求出最高工资，再在「小于最高工资」的集合里取 `MAX`。
- 边界情况（工资种类不够）时，两种写法都会自然返回 `NULL`。

**解法一：子查询 + LIMIT / OFFSET（推荐）**

```sql
SELECT
    (
        SELECT DISTINCT Salary
        FROM Employee
        ORDER BY Salary DESC
        LIMIT 1 OFFSET 1
    ) AS SecondHighestSalary;
```

- `DISTINCT Salary`：只看不同工资值。
- `ORDER BY Salary DESC`：从高到低排。
- `LIMIT 1 OFFSET 1`：跳过最高的那条，取下一条（即第二高）。
- 标量子查询在没有结果时会返回 `NULL`，符合题意。

**解法二：用 MAX 和「小于最高工资」的条件**

```sql
SELECT
    MAX(Salary) AS SecondHighestSalary
FROM Employee
WHERE Salary < (
    SELECT MAX(Salary) FROM Employee
);
```

- 内层 `SELECT MAX(Salary)` 求最高工资。
- 外层 `WHERE Salary < 最高工资` 过滤掉最高工资行，在剩余行里取最大值 → 即第二高。
- 若没有比最高工资更小的工资（工资种类不够），外层集合为空，`MAX` 结果为 `NULL`。

**本题知识点总结：**

- **DISTINCT 去重：**
  - 「第 n 高工资」通常指按「不同工资」排序，习惯先 `DISTINCT Salary`。
- **ORDER BY + LIMIT / OFFSET：**
  - 第 1 高：`LIMIT 1 OFFSET 0`
  - 第 2 高：`LIMIT 1 OFFSET 1`
  - 第 n 高：`LIMIT 1 OFFSET n-1`
- **标量子查询的返回值：**
  - 子查询返回 0 行时，结果为 `NULL`，可以直接作为一列使用。
- **聚合函数在空集上的结果：**
  - `MAX()` 等聚合函数在空集上返回 `NULL`，可以自然处理「不存在第二高」的情况。
- **子查询两种位置：**
  - `SELECT (...)` 中当作一列；
  - `WHERE` 中用于比较（如 `WHERE col < (SELECT MAX(...))`）。

**「第 N 高」通用模版（LIMIT 版）：**

```sql
SELECT
    (
        SELECT DISTINCT 列名
        FROM 表名
        ORDER BY 列名 DESC
        LIMIT 1 OFFSET N-1
    ) AS 第N高别名;
```

**「第二高」通用模版（MAX + 小于最大值版）：**

```sql
SELECT
    MAX(列名) AS 第二高别名
FROM 表名
WHERE 列名 < (
    SELECT MAX(列名) FROM 表名
);
```

---

## 示例：LeetCode 185. 部门工资前三高的员工

**表结构：**

`Employee`
```text
+--------------+---------+
| id           | int     |  主键
| name         | varchar |
| salary       | int     |
| departmentId | int     |  外键，指向 Department.id
+--------------+---------+
```

`Department`
```text
+-------------+---------+
| id          | int     |  主键
| name        | varchar |
+-------------+---------+
```

**题目要求：**

查出每个部门工资前三高的员工，输出列：`Department`（部门名）、`Employee`（员工名）、`Salary`（工资）。同一部门内工资相同则同排名，且仍算「前三」（例如两人并列第一，则下一名是第二，不是第三）。

**思路（人话版）：**

- 需要「按部门分组、组内按工资从高到低排名」，且只保留排名 ≤ 3 的人。
- 用 **窗口函数** `DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY salary DESC)` 在每条员工记录上打上「部门内排名」。
- 先做 `Employee LEFT JOIN Department` 得到「员工 + 部门名」，再在子查询里算 `rn`，外层 `WHERE rn <= 3` 过滤出前三。

**标准解法 SQL：**

```sql
-- 外层查询：充当 WHERE 过滤，只保留部门内排名 ≤ 3
SELECT
    Department,
    Employee,
    Salary
FROM (
    -- 内层查询（子查询）：先执行，完成连表 + 打排名标签
    SELECT
        d.name   AS Department,
        e.name   AS Employee,
        e.salary AS Salary,
        DENSE_RANK() OVER (
            PARTITION BY e.departmentId
            ORDER BY e.salary DESC
        ) AS rn
    FROM Employee e
    LEFT JOIN Department d ON e.departmentId = d.id
) temp
WHERE rn <= 3;
```

**为什么不能直接在外层用 WHERE rn？**

- 在标准 SQL 里，`SELECT` 里定义的别名（如 `rn`）在**同一条 SELECT 对应的 WHERE 中不可用**（WHERE 在 SELECT 之前执行）。
- 所以要把「连表 + 窗口函数算 rn」放在子查询里，外层对子查询结果再 `WHERE rn <= 3`。

**本题知识点总结：**

- **窗口函数 DENSE_RANK()：**
  - `DENSE_RANK() OVER (PARTITION BY 分组列 ORDER BY 排序列 [DESC])`：按分组列分组，组内按排序列排序后打密集排名（同分同排名，下一名不跳号）。
  - 与 `ROW_NUMBER()` 区别：同分时 ROW_NUMBER 会 1,2,3，DENSE_RANK 会 1,1,2；题目要求「前三高」允许并列，用 DENSE_RANK 更合适。
- **子查询 + 别名：**
  - 内层 SELECT 产生带 `rn` 的结果集，外层才能用 `WHERE rn <= 3`。
- **SQL 执行顺序（便于理解「为什么 rn 要放子查询」）：**
  - 先执行 **FROM**（加载表/子查询结果）→ **WHERE**（筛选）→ **GROUP BY**（分组）→ **SELECT**（包括窗口函数的计算）→ **ORDER BY**。
  - 因此同一层 SELECT 里算出的别名，不能在同一层的 WHERE 里使用，需要多一层子查询。

**「每个分组内 Top K」通用模版（窗口函数版）：**

```sql
SELECT 分组标识, 要输出的列
FROM (
    SELECT
        分组标识,
        要输出的列,
        DENSE_RANK() OVER (
            PARTITION BY 分组列
            ORDER BY 排序列 DESC
        ) AS rn
    FROM 表名 [JOIN ...]
) t
WHERE rn <= K;
```

---

## 后续扩展建议

后续你在刷其它数据库题（尤其是 LeetCode 数据库 / 字节机试题库）时，可以：

- 按「题目模板」章节的格式，将每道题追加到本文档末尾。
- 尝试在「知识点总结」部分整理：
  - 使用了哪种 JOIN / GROUP BY / HAVING / ORDER BY / LIMIT 等；
  - 是否涉及窗口函数（如 `ROW_NUMBER()`）、子查询、聚合函数等。

最终，这个文档会成为你的 **「数据库机试速查小抄」**。


