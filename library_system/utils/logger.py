# -*- coding: utf-8 -*-
"""
日志工具模块 - Logger Utility Module

提供系统运行日志记录功能。

设计说明：
- 单例模式确保全局唯一的日志记录器
- 支持不同日志级别：DEBUG, INFO, WARNING, ERROR
- 日志输出到文件和控制台
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class Logger:
    """
    日志记录器类（单例模式）
    
    示例：
        >>> logger = Logger.get_instance()
        >>> logger.info("System started")
        >>> logger.error("An error occurred")
    """
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """初始化日志记录器"""
        if self._initialized:
            return
        
        # 日志目录
        log_dir = Path.home() / '.library_system' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建logger
        self._logger = logging.getLogger('LibrarySystem')
        self._logger.setLevel(logging.DEBUG)
        
        # 避免重复添加handler
        if not self._logger.handlers:
            # 文件处理器
            log_file = log_dir / f'system_{datetime.now().strftime("%Y%m%d")}.log'
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # 格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)
        
        self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Logger':
        """获取日志记录器实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def debug(self, message: str) -> None:
        """记录调试信息"""
        self._logger.debug(message)
    
    def info(self, message: str) -> None:
        """记录一般信息"""
        self._logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录警告信息"""
        self._logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录错误信息"""
        self._logger.error(message)
    
    def critical(self, message: str) -> None:
        """记录严重错误"""
        self._logger.critical(message)
