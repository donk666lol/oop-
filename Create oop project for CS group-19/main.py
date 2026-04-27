from storage.data_manager import DataManager
from storage.data_initializer import DataInitializer
from models.library import Library
from services.library_service import LibraryService
from ui.menu_system import MenuSystem

def main():
    library = Library()
    service = LibraryService(library)
    data_mgr = DataManager()

    if data_mgr.file_exists():
        print("检测到已有数据，正在加载...")
        data = data_mgr.load()
        if data:
            # 加载已有数据
            service.load_data(data)  # 需要B同学实现这个方法
    else:
        print("首次运行，正在生成初始化数据...")
        books, members = DataInitializer.generate()
        for book in books:
            library.add_book(book)
        for member in members:
            library.add_member(member)
        print(f"初始化完成！{len(books)} 本书, {len(members)} 个会员")
        # 首次运行也要保存一次
        service.save_data()

    menu = MenuSystem(service)
    menu.run()

if __name__ == "__main__":
    main()

