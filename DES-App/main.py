"""Main.py Application Entry Point"""

"""Import Statements"""
from window import GUIManager

"""Main Application Function"""
def main():
    gui_manager = GUIManager()
    window = gui_manager.create_main_menu()
    gui_manager.handle_events()

if __name__ == '__main__':
    main()