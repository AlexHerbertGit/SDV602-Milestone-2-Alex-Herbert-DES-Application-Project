""" 
GUI Manager and DES window creation Class

"""

"""Chart Manager Import Statments"""
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from charts import ChartManager
import matplotlib.pyplot as plt
from data_manager import DataManager
from user_manager import UserManager

"""GUIManager Class instantiation"""
class GUIManager:
    def __init__(self, user_manager, data_manager):
        self.user_manager = user_manager
        self.chart_manager = ChartManager()
        self.data_manager = data_manager
        self.current_des_index = 0
        self.uploaded_file_path = None
        self.current_user = None
        self.des_windows = [
            self.chart_manager.draw_line_chart,
            self.chart_manager.draw_bar_chart,
            self.chart_manager.draw_scatter_plot
        ]

    """Main Menu Window Creation"""
    def create_main_menu(self):          
        layout = [
            [sg.Text("Main Menu", font=("Helvetica", 16), justification="center")],
            [sg.Button("Register"), sg.Button("Login")],
            [sg.Button ("Open DES 1"), sg.Button("Open DES 2"), sg.Button("Open DES 3")],
            [sg.Button("Log Out")],
            [sg.Text(f"Username: {self.current_user}")],
            [sg.Button("Close Application")]
        ]
        return sg.Window("Main Menu", layout, finalize=True)

    """DES Window Creation"""
    def create_des_window(self, chart_function, figure_canvas_agg=None):           
        figure_h = 600
        figure_w = 1000
        
        
        left_column = [             #Left Column Navigation
            [sg.Button("Next", size=(10, 1))],
            [sg.Button("Previous", size=(10, 1))],
            [sg.Button("Home", size=(10, 1))]
        ]
        
        
        right_column = [            #Right Column Options and Data Source Selection and Upload
            [sg.Button ("Set Data Source", size=(15, 1))],
            [sg.Button("Upload Data Source", size=(15, 1))],
            [sg.Button("Upload to Remote", size=(15, 1))],
            [sg.Button("Fetch from Remote", size=(15, 1))],
            [sg.Button("Chart Settings", size=(15, 1))],
            [sg.Button("Zoom +", size=(15,1))],
            [sg.Button("Zoom -", size=(15, 1))]
        ]

        
        chart_canvas = [[sg.Canvas(size=(figure_w, figure_h), key="-CANVAS-")]]         #Canvas for graphs in the center column

        
        summary_section = [             #Summary Section
            [sg.Text("Graph Summary Information", justification="center")],
            [sg.Text("Field One:"), sg.InputText(key="-FIELD1-", size=(20, 1))],
            [sg.Text("Field Two:"), sg.InputText(key="-FIELD2-", size=(20, 1))]
        ]

        
        chat_section = [            #Chat Section and User input
            [sg.Text("Chat")],
            [sg.Multiline(size=(60, 5), key="-CHAT-", disabled=True)],
            [sg.Input(key="-CHAT_INPUT-", size=(50, 1)), sg.Button("Send")]
        ]

        
        layout = [          #DES Layout for GUI
            [
                sg.Column(left_column, vertical_alignment="top"),
                sg.Column(chart_canvas, justification="center"),
                sg.Column(right_column, vertical_alignment="top")
            ],
            [sg.Column(summary_section, justification="center")],
            [sg.Column(chat_section, justification="center")]
        ]

       
        window = sg.Window("Data Explorer Screen", layout, finalize=True)            #Create the DES window
        
        
        if figure_canvas_agg is not None:           #Delete existing figure from previous screen if it exists
            figure_canvas_agg.get_tk_widget().forget()

        
        plt.clf()           #Clears the current figure from the canvas to make sure the new one is being drawn

       
        fig = chart_function()           #Draw chart from ChartManager using passed-in chart function
        figure_canvas_agg = self.draw_figure(window['-CANVAS-'].TKCanvas, fig)

        return window, figure_canvas_agg
    
    def create_registration_window(self):
        layout = [
            [sg.Text("Register a New Account")],
            [sg.Text("Username:", size=(10, 1)), sg.InputText(key="-USERNAME-")],
            [sg.Text("Password:", size=(10, 1)), sg.InputText(key="-PASSWORD-", password_char="*")],
            [sg.Button("Submit"), sg.Button("Back")]
        ]
        return sg.Window("Register", layout, finalize=True)
    
    def create_login_window(self):
        layout = [
            [sg.Text("Login to Your Account")],
            [sg.Text("Username:", size=(10, 1)), sg.InputText(key="-USERNAME-")],
            [sg.Text("Password:", size=(10, 1)), sg.InputText(key="-PASSWORD-", password_char="*")],
            [sg.Button("Submit"), sg.Button("Back")]
        ]
        return sg.Window("Login", layout, finalize=True)

    """Draw Figure Function"""
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg

    def register_user(self, username, password):
        max_length = 255
        if len(username) > max_length or len(password) > max_length:
            sg.popup(f"Username and password must not exceed {max_length} characters.")
            return

        example = [{"username": "string(255)", "password": "string(255)"}]
        self.jsn_drop_service.create("users", example)

        values = [{"username": username, "password": password}]
        response = self.jsn_drop_service.store("users", values)
        
        if response is not None:
            sg.popup("User registered successfully!")
        else:
            sg.popup("Failed to register user. Check console for details.")

    def login_user(self, username, password):
        users = self.jsn_drop_service.all("users")
        for user in users:
            if user["username"] == username and user["password"] == password:
                self.current_user = username 
                sg.popup("Login Successful!")
                return True
        sg.popup("login failed. Please check login credentials.")
        return False

    """Event Handler Function"""
    def handle_events(self):
        window = self.create_main_menu()
        figure_canvas_agg = None

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "Close Application"):
                break
            elif event == "Open DES 1":
                self.current_des_index = 0
                self.user_manager.set_current_DES(0) 
                window.close()
                #Pass line_plot function as the chart_function parameter
                window, figure_canvas_agg = self.create_des_window(self.chart_manager.draw_line_chart, figure_canvas_agg)
            elif event == "Open DES 2":
                self.current_des_index = 1
                self.user_manager.set_current_DES(1) 
                window.close()
                #Pass bar_chart function as the chart_function parameter
                window, figure_canvas_agg = self.create_des_window(self.chart_manager.draw_bar_chart, figure_canvas_agg)
            elif event == "Open DES 3":
                self.current_des_index = 2
                self.user_manager.set_current_DES(2) 
                window.close()
                #Pass scatter_plot function as the chart_function parameter
                window, figure_canvas_agg = self.create_des_window(self.chart_manager.draw_scatter_plot, figure_canvas_agg)
            elif event == "Next":
                window.close()
                #Increment the current_des_index and cycle through DES windows
                self.current_des_index = (self.current_des_index + 1) % len(self.des_windows)
                window, figure_canvas_agg = self.create_des_window(self.des_windows[self.current_des_index], figure_canvas_agg)
            elif event == "Previous":
                window.close()
                #Decrement the current_des_index and cycle back through DES windows
                self.current_des_index = (self.current_des_index - 1) %len(self.des_windows)
                window, figure_canvas_agg = self.create_des_window(self.des_windows[self.current_des_index], figure_canvas_agg)
            elif event == "Home":
                window.close()
                window = self.create_main_menu()
            elif event == "Upload Data Source":
                file_path = sg.popup_get_file("Select Data File", file_types=(("CSV Files", "*.csv"),))
                if file_path:
                    self.uploaded_file_path = file_path
                    data = self.data_manager.read_local_data(self.uploaded_file_path)
                    if data is not None:
                        sg.popup("Data Uploaded Successfully!", title="Success")
            elif event == "Set Data Source":
                if self.uploaded_file_path:
                    data = self.data_manager.read_local_data(self.uploaded_file_path)
                    if data is not None:
                        sg.popup("Data Source Set Successfully!", title="Success")
                        window["-FIELD1-"].update(self.data_manager.get_data_summary())

                        # Update the chart with the new data
                        plt.clf()
                        fig = self.des_windows[self.current_des_index](data)
                        figure_canvas_agg.get_tk_widget().forget()
                        figure_canvas_agg = self.draw_figure(window["-CANVAS-"].TKCanvas, fig)
                    else:
                        sg.popup("Failed to load data. Please upload a valid file.", title="Error")
                else:
                    sg.popup("No data source uploaded. Please upload a data source first.", title="Error")
            elif event == "Upload to Remote":
                if self.uploaded_file_path:
                    dataset_name = sg.popup_get_text("Enter a name for the dataset:", title="Dataset Name")
                    dataset_type = sg.popup_get_text("Enter the type of the dataset (e.g., Bar Chart, Line Chart):", title="Dataset Type")
                    
                    if dataset_name and dataset_type:
                        message = self.data_manager.upload_to_remote("des_data_sources", dataset_name, dataset_type, self.uploaded_file_path)
                        sg.popup(message, title="Upload Status")
                    else:
                        sg.popup("Dataset name and type are required.", title="Error")
                else:
                    sg.popup("No local dataset available. Please upload a dataset first.", title="Error")
                    
            elif event == "Fetch from Remote":
                #Fetch data source from JsnDrop database
                result = self.data_manager.fetch_from_remote("des_data_sources")
                if "successfully" in result.lower():
                    #Merge the remote data source with the local one
                    self.data_manager.merge_data(self.data_manager.remote_data)
                    sg.popup("Remote data fetched and merged with local data successfully.")
                else:
                    sg.popup(fetch_result)
            elif event == "Send":
                # Get the message from the input field
                message = values["-CHAT_INPUT-"]
                if message:
                    # Add message to the current DES chat
                    result = self.user_manager.chat(message)
                    if result == "Chat sent":
                        # Fetch and display updated chat messages
                        messages = self.user_manager.get_chat()
                        if messages:
                            chat_text = "\n".join([f"{msg['PersonID']}: {msg['Chat']}" for msg in messages])
                            window["-CHAT-"].update(chat_text)
                    else:
                        sg.popup(result)
                    window["-CHAT_INPUT-"].update("")  # Clear the input field
            elif event == "Register":
                # Handle Registration
                window.close()
                registration_window = self.create_registration_window()
                while True:
                    reg_event, reg_values = registration_window.read()
                    if reg_event in (sg.WIN_CLOSED, "Back"):
                        registration_window.close()
                        window = self.create_main_menu()
                        break
                    elif reg_event == "Submit":
                        username = reg_values["-USERNAME-"]
                        password = reg_values["-PASSWORD-"]
                        result = self.user_manager.register(username, password)
                        sg.popup(result)
            elif event == "Login":
                # Handle Login
                window.close()
                login_window = self.create_login_window()
                while True:
                    login_event, login_values = login_window.read()
                    if login_event in (sg.WIN_CLOSED, "Back"):
                        login_window.close()
                        window = self.create_main_menu()
                        break
                    elif login_event == "Submit":
                        username = login_values["-USERNAME-"]
                        password = login_values["-PASSWORD-"]
                        result = self.user_manager.login(username, password)
                        sg.popup(result)
                        if result == "Login Success":
                            self.current_user = username
                            login_window.close()
                            window = self.create_main_menu()
                            break

            elif event == "Logout":
                # Handle Logout
                result = self.user_manager.logout()
                sg.popup(result)
                self.current_user = None

        window.close()  