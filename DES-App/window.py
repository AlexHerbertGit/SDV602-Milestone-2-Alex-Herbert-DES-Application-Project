#Chart Manager Import Statments
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from charts import ChartManager

#GUIManager Class instantiation
class GUIManager:
    def __init__(self):
        self.chart_manager = ChartManager()
        self.current_des_index = 0
        self.des_windows = [
            self.chart_manager.draw_line_chart,
            self.chart_manager.draw_bar_chart,
            self.chart_manager.draw_scatter_plot
        ]

    #Main Menu Window Creation
    def create_main_menu(self):
        layout = [
            [sg.Text("Main Menu", font=("Helvetica", 16), justification="center")],
            [sg.Button ("Open DES 1"), sg.Button("Open DES 2"), sg.Button("Open DES 3")],
            [sg.Button("Log Out")],
            [sg.Text("Username: User 1")],
            [sg.Button("Close Application")]
        ]
        return sg.Window("Main Menu", layout, finalize=True)

    #DES Window Creation
    def create_des_window(self, chart_function):
        figure_h = 650
        figure_w = 650
        layout = [
            [sg.Button("Next"), sg.Button("Previous"), sg.Button("Home")],
            [sg.Canvas(size=(figure_w, figure_h), key="-CANVAS-")],
            [sg.Text("Graph Summary Information"), sg.Text("Field One:"), sg.Text("Field Two:")],
            [sg.Multiline(size=(60, 5), key="-CHAT-")],
            [sg.Input(key="-INPUT-"), sg.Button("Send")]
        ]
        window = sg.Window("Data Explorer Screen", layout, finalize=True)
        figure_canvas_agg = None

        #Draw chart from ChartManager using passed-in chart function
        fig = chart_function()
        figure_canvas_agg = self.draw_figure(window['-CANVAS-'].TKCanvas, fig)

        return window, figure_canvas_agg

    #Draw Figure Function
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
        return figure_canvas_agg

    #Event Handler Function
    def handle_events(self):
        window = self.create_main_menu()

        while True:
            event, values = window.read()

            if event in (sg.WIN_CLOSED, "Close Application"):
                break

            elif event == "Open DES 1":
                self.current_des_index = 0 
                window.close()
                #Pass line_plot function as the chart_function parameter
                window, fig_canvas = self.create_des_window(self.chart_manager.draw_line_chart)

            elif event == "Open DES 2":
                self.current_des_index = 1
                window.close()
                #Pass bar_chart function as the chart_function parameter
                window, fig_canvas = self.create_des_window(self.chart_manager.draw_bar_chart)

            elif event == "Open DES 3":
                self.current_des_index = 2
                window.close()
                #Pass scatter_plot function as the chart_function parameter
                window, fig_canvas = self.create_des_window(self.chart_manager.draw_scatter_plot)

            elif event == "Next":
                window.close()
                #Increment the current_des_index and cycle through DES windows
                self.current_des_index = (self.current_des_index + 1) % len(self.des_windows)
                window, fig_canvas = self.create_des_window(self.des_windows[self.current_des_index])

            elif event == "Previous":
                window.close()
                #Decrement the current_des_index and cycle back through DES windows
                self.current_des_index = (self.current_des_index - 1) %len(self.des_windows)
                window, fig_canvas = self.create_des_window(self.des_windows[self.current_des_index])
                
            elif event == "Home":
                window.close()
                window = self.create_main_menu()

            elif event == "Send":
                #Logic for chat/message functionality placeholder
                chat_text = values["-INPUT-"]
                window["-CHAT-"].print(f"User: {chat_text}")

        window.close()  