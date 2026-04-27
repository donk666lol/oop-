import json
from double_linked_list import DoubleLinkedList
from models import BooksNode

# 保存数据
def save_data(linked_list, filename='library.json'):
    data = linked_list.to_list()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("💾 数据已保存")

# 加载数据
def load_data(filename='library.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        ll = DoubleLinkedList()
        for b in data:
            node = BooksNode(b['title'], b['author'], b['version'], b['book_id'])
            ll.add_books(node)
        print("📂 数据已加载")
        return ll
    except:
        print("📂 无数据，新建图书库")
        return DoubleLinkedList()