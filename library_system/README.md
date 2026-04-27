# 图书馆管理系统 - Library Management System

## 项目简介

这是一个基于Python的面向对象图书馆管理系统，用于管理图书、用户和借阅记录。本项目是JC1503面向对象编程课程的小组项目。

## 功能特性

### 图书管理
- ✅ 添加、更新、删除图书
- ✅ 按ID、书名、作者、分类搜索图书
- ✅ 查看图书详细信息
- ✅ 图书分类层次结构管理

### 用户管理
- ✅ 注册、更新、删除用户
- ✅ 支持多种用户类型（学生、教师、职工、管理员）
- ✅ 用户借阅权限管理
- ✅ 用户状态管理（正常、暂停、删除）

### 借阅管理
- ✅ 借书、还书功能
- ✅ 续借功能
- ✅ 图书预约功能
- ✅ 逾期检测和罚款计算
- ✅ 借阅历史记录

### 数据持久化
- ✅ JSON格式数据存储
- ✅ 自动数据备份
- ✅ 数据导入导出

## 技术实现

### 面向对象概念
- **类与对象**: Book, User, BorrowRecord等实体类
- **封装**: 私有属性 + @property访问器
- **继承**: TreeNode继承，异常类继承
- **多态性**: 不同用户类型的借阅行为差异
- **组合关系**: LibrarySystem包含Book和User集合
- **抽象类**: 自定义异常基类
- **自定义异常**: 完整的异常层次结构

### 数据结构实现
| 数据结构 | 实现文件 | 应用场景 |
|----------|----------|----------|
| 双向链表 | doubly_linked_list.py | 借阅记录存储 |
| 栈 | stack.py | 操作历史（撤销功能） |
| 队列 | queue.py | 借阅请求队列 |
| 通用树 | tree.py | 图书分类层次 |
| 二叉搜索树 | binary_search_tree.py | 书名索引 |
| 哈希表 | hash_table.py | 快速查找 |

### 算法实现
- 递归树遍历（前序、中序、后序）
- 范围查询（BST）
- 括号匹配检查（栈应用）
- 字符串反转（栈应用）

## 项目结构

```
library_system/
├── main.py                    # 程序入口
├── core/                      # 核心模块
│   ├── __init__.py
│   ├── exceptions.py          # 自定义异常
│   ├── library_system.py      # 主系统类
│   └── data_manager.py        # 数据持久化
├── datastructures/            # 数据结构
│   ├── __init__.py
│   ├── doubly_linked_list.py
│   ├── stack.py
│   ├── queue.py
│   ├── tree.py
│   ├── binary_search_tree.py
│   └── hash_table.py
├── entities/                  # 实体类
│   ├── __init__.py
│   ├── book.py
│   ├── user.py
│   └── borrow_record.py
├── utils/                     # 工具模块
│   ├── __init__.py
│   └── logger.py
├── tests/                     # 测试
│   └── test_system.py
├── 团队分工大纲.md              # 分工文档
└── README.md                  # 本文件
```

## 运行方法

```bash
# 进入项目目录
cd library_system

# 运行程序
python main.py
```

## 运行测试

```bash
# 运行所有测试
python -m pytest tests/

# 或使用unittest
python tests/test_system.py
```

## 系统要求

- Python 3.8+
- 无需额外依赖（使用标准库）

## 团队成员

| 成员 | 职责 |
|------|------|
| 成员A | 系统架构与核心模块 |
| 成员B | 数据结构模块 |
| 成员C | 实体类模块 |
| 成员D | 用户界面与测试 |
| 成员E | 工具模块与文档 |

## 开发时间线

- **2026年3月16日**: 组建小组截止
- **2026年5月8日**: 最终提交截止

## 提交物

1. ✅ 完整源代码
2. ⏳ 主报告（LaTeX，最多10页）
3. ⏳ 演示视频（≤10分钟）
4. ⏳ 流程演示视频（≤10分钟）

## 许可证

本项目仅用于教育目的，属于JC1503课程作业。
