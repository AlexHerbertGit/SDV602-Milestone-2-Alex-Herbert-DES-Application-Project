"""Main.py Application Entry Point"""

"""Import Statements"""
from window import GUIManager
from user_manager import UserManager
from data_manager import DataManager
from jsn_drop_service import jsnDrop

"""Main Application Function"""
def main():

    jsn_drop_service = jsnDrop(
        tok="39d0f8d6-bb55-4158-b364-72a33642e8ef",
        url="https://newsimland.com/~todd/JSON"
    )

    user_manager = UserManager()
    data_manager = DataManager(jsn_drop_service)

    gui_manager = GUIManager(user_manager, data_manager)

    window = gui_manager.create_main_menu()
    gui_manager.handle_events()

if __name__ == '__main__':
    main()