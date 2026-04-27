# -*- coding: utf-8 -*-
"""
数据管理模块 - Data Manager Module

负责数据的持久化存储和加载，支持JSON格式文件存储。

设计说明：
- 单例模式确保全局唯一的数据管理器
- 支持数据的导入和导出
- 处理文件读写异常
"""

import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


class DataManager:
    """
    数据管理器类
    
    负责数据的持久化存储和加载。
    
    属性：
        data_dir: 数据存储目录
        backup_dir: 备份目录
    
    示例：
        >>> dm = DataManager()
        >>> dm.save_data({'books': [], 'users': []})
        >>> data = dm.load_data()
    """
    
    _instance: Optional['DataManager'] = None
    
    def __new__(cls, data_dir: str = None):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, data_dir: str = None):
        """初始化数据管理器"""
        if self._initialized:
            return
        
        self._data_dir = Path(data_dir) if data_dir else Path.home() / '.library_system' / 'data'
        self._backup_dir = self._data_dir / 'backups'
        
        # 确保目录存在
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._backup_dir.mkdir(parents=True, exist_ok=True)
        
        self._data_file = self._data_dir / 'library_data.json'
        
        self._initialized = True
    
    def has_saved_data(self) -> bool:
        """检查是否有已保存的数据"""
        return self._data_file.exists() and self._data_file.stat().st_size > 0
    
    def save_data(self, data: Dict[str, Any]) -> bool:
        """
        保存数据到文件
        
        参数：
            data: 要保存的数据字典
            
        返回：
            bool: 保存成功返回True
        """
        try:
            # 先创建备份
            if self._data_file.exists():
                self._create_backup()
            
            # 保存新数据
            with open(self._data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            print(f"[错误] 保存数据失败: {e}")
            return False
    
    def load_data(self) -> Optional[Dict[str, Any]]:
        """
        从文件加载数据
        
        返回：
            Optional[Dict]: 加载的数据，如果失败返回None
        """
        try:
            if not self._data_file.exists():
                return None
            
            with open(self._data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
                
        except Exception as e:
            print(f"[错误] 加载数据失败: {e}")
            return None
    
    def _create_backup(self) -> None:
        """创建数据备份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self._backup_dir / f'library_data_{timestamp}.json'
        
        try:
            import shutil
            shutil.copy2(self._data_file, backup_file)
            
            # 清理旧备份（保留最近10个）
            backups = sorted(self._backup_dir.glob('library_data_*.json'))
            while len(backups) > 10:
                backups[0].unlink()
                backups.pop(0)
                
        except Exception as e:
            print(f"[警告] 创建备份失败: {e}")
    
    def export_data(self, export_path: str) -> bool:
        """导出数据到指定路径"""
        try:
            if not self._data_file.exists():
                return False
            
            import shutil
            shutil.copy2(self._data_file, export_path)
            return True
            
        except Exception as e:
            print(f"[错误] 导出数据失败: {e}")
            return False
    
    def import_data(self, import_path: str) -> bool:
        """从指定路径导入数据"""
        try:
            import shutil
            shutil.copy2(import_path, self._data_file)
            return True
            
        except Exception as e:
            print(f"[错误] 导入数据失败: {e}")
            return False
    
    def clear_data(self) -> bool:
        """清除所有数据"""
        try:
            if self._data_file.exists():
                self._data_file.unlink()
            return True
            
        except Exception as e:
            print(f"[错误] 清除数据失败: {e}")
            return False
