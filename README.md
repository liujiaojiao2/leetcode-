# 数据结构与算法 · LeetCode 刷题

在本项目中按难度整理 LeetCode 题目与题解，便于复习和检索。

## 目录结构

```
data_struct/
├── README.md
├── leetcode/
│   ├── template.py      # 做题模板（复制后改题号与解法）
│   ├── easy/            # 简单题
│   ├── medium/          # 中等题
│   └── hard/            # 困难题
```

## 使用方式

### 1. 新建一题

- 复制 `leetcode/template.py` 到对应难度目录下。
- 文件名建议：`题号_题目英文名.py`，例如 `001_two_sum.py`。
- 在文件头部填写题目链接、描述和思路，在 `Solution` 里实现解法。
- 在 `if __name__ == "__main__":` 里写本地测试用例（可加 `assert` 自测）。

### 2. 运行与自测

在项目根目录下执行（替换为你的文件路径）：

```bash
# 运行某一道题
python leetcode/easy/001_two_sum.py
```

若使用断言，通过则无输出，失败会报错。

### 3. 提交到 LeetCode

- 只把 `Solution` 类中对应的方法复制到 LeetCode 编辑器提交即可。
- 类名保持 `Solution`，方法名和参数与题目要求一致。

## 示例

`leetcode/easy/001_two_sum.py` 是「两数之和」的完整示例，包含题目说明、解法和本地测试，可直接运行参考。

## 建议

- 每道题先写思路再写代码，方便日后复习。
- 同一题多种解法可写在同一个文件里（如 `twoSum_v2`），或注明在注释中。
- 按专题刷（数组、链表、二叉树、DP 等）时，可在对应难度下再建子目录，如 `easy/array/`。

祝刷题顺利。
