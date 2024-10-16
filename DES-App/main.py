#Main.py Application Entry Point

from window import GUIManager

def main():
    gui_manager = GUIManager()
    window = gui_manager.create_main_menu()
    qui_manager.handle_events(window)

if __name__ == '__main__':
    main()