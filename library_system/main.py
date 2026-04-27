# -*- coding: utf-8 -*-
"""
Library Management System - 主程序入口
Library Management System - Main Entry Point

这个模块是整个图书馆管理系统的入口点，负责初始化系统并启动用户界面。

主要功能：
- 初始化数据持久化层
- 创建主系统实例
- 启动用户交互界面
"""

from core.library_system import LibrarySystem
from core.data_manager import DataManager
from utils.logger import Logger

# 系统版本信息
__version__ = "1.0.0"
__author__ = "OOP Group Project Team"

def main():
    """
    系统主入口函数
    
    程序启动流程：
    1. 初始化日志系统
    2. 创建数据管理器实例
    3. 创建图书馆系统实例
    4. 启动用户界面
    
    数据持久化：
    - 首次运行：自动生成示例数据并保存到文件
    - 后续运行：从文件加载已有数据
    """
    logger = Logger.get_instance()
    logger.info("=" * 50)
    logger.info("Library Management System Starting...")
    logger.info(f"Version: {__version__}")
    logger.info("=" * 50)
    
    # 创建数据管理器（负责数据持久化）
    data_manager = DataManager()
    
    # 创建图书馆系统实例
    library = LibrarySystem(data_manager)
    
    # 启动用户界面
    library.run()
    
    logger.info("Library Management System Shutdown.")


if __name__ == "__main__":
    main()
