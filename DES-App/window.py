""" 
GUI Manager and DES window creation Class

"""

"""Chart Manager Import Statments"""
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from charts import ChartManager
import matplotlib.pyplot as plt
from data_manager import DataManager

"""GUIManager Class instantiation"""
class GUIManager:
    def __init__(self):
        self.chart_manager = ChartManager()
        self.data_manager = DataManager()
        self.current_des_index = 0
        self.uploaded_file_path = None
        self.des_windows = [
            self.chart_manager.draw_line_chart,
            self.chart_manager.draw_bar_chart,
            self.chart_manager.draw_scatter_plot
        ]

    """Main Menu Window Creation"""
    def create_main_menu(self):          
        layout = [
            [sg.Text("Main Menu", font=("Helvetica", 16), justification="center")],
            [sg.Button ("Open DES 1"), sg.Button("Open DES 2"), sg.Button("Open DES 3")],
            [sg.Button("Log Out")],
            [sg.Text("Username: User 1")],
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
            [sg.Multiline(size=(60, 5), key="-CHAT-")],
            [sg.Input(key="-INPUT-"), sg.Button("Send")]
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

    """Draw Figure Function"""
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg

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
                window.close()
                #Pass line_plot function as the chart_function parameter
                window, figure_canvas_agg = self.create_des_window(self.chart_manager.draw_line_chart, figure_canvas_agg)
            elif event == "Open DES 2":
                self.current_des_index = 1
                window.close()
                #Pass bar_chart function as the chart_function parameter
                window, figure_canvas_agg = self.create_des_window(self.chart_manager.draw_bar_chart, figure_canvas_agg)
            elif event == "Open DES 3":
                self.current_des_index = 2
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
            elif event == "Send":
                #Logic for chat/message functionality placeholder
                chat_text = values["-INPUT-"]
                window["-CHAT-"].print(f"User: {chat_text}")

        window.close()  