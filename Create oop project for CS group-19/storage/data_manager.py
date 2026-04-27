import json
from pathlib import Path

class DataManager:
    def __init__(self, filepath="data/library_data.json"):
        self._filepath = filepath
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    def save(self, data):
        with open(self._filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已保存 {len(data.get('books', []))} 本书, {len(data.get('members', []))} 个会员")

    def load(self):
        if not Path(self._filepath).exists():
            print("第一次运行，需要初始化数据")
            return None
        with open(self._filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"已加载 {len(data.get('books', []))} 本书, {len(data.get('members', []))} 个会员")
        return data

    def file_exists(self):
        return Path(self._filepath).exists()
