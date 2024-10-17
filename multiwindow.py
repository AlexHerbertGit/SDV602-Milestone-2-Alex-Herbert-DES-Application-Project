from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ChartExamples as ce
import PySimpleGUI as sg
import matplotlib as plt

import inspect
plt.use('TkAgg')
"""
    Demo - 2 simultaneous windows using read_all_window

    Both windows are immediately visible.  Each window updates the other.

    Copyright 2020 PySimpleGUI.org
"""

current_window = 0
max_windows = 2
list_of_window_references = {}
figure_agg = None


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    plt.pyplot.close('all')


def make_win1():
    global figure_agg
    figure_h = 650
    figure_w = 650
    layout = [[sg.Text('Window 1')],
              [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
              [sg.Text('Enter something to output to Window 2')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25, 1), key='-OUTPUT-')],
              [sg.Button('Reopen')],
              [sg.Button('Prev'), sg.Button('Next')],
              [sg.Button('Exit')]]
    window = sg.Window('Window Title', layout, finalize=True)
    if figure_agg:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(figure_agg)
        figure_agg = None
    # # call function to get the figure

    fig = ce.line_plot()
    figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    return window


def make_win2():
    global figure_agg
    figure_w = 650
    figure_h = 650
    layout = [[sg.Text('Window 2')],

              [sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')],
              [sg.Text('Enter something to output to Window 1')],
              [sg.Input(key='-IN-', enable_events=True)],
              [sg.Text(size=(25, 1), key='-OUTPUT-')],
              [sg.Button('Prev'), sg.Button('Next')],
              [sg.Button('Exit')]]

    window2 = sg.Window('Window Title', layout, finalize=True)
    if figure_agg:
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(figure_agg)
        figure_agg = None
    # # call function to get the figure

    fig = ce.discrete_plot()
    figure_agg = draw_figure(window2['-CANVAS-'].TKCanvas, fig)

    return window2


def show_current_window():
    for i in range(0, max_windows):
        if i != current_window:
            list_of_window_references[i].Hide()
    list_of_window_references[current_window].UnHide()


def main():
    global current_window

    figure_agg = None
    list_of_window_references[0], list_of_window_references[1] = make_win1(
    ), make_win2()

    # list_of_window_references[1].move(list_of_window_references[1].current_location()[
    #    0], list_of_window_references[0].current_location()[1]+220)

    show_current_window()

    while True:             # Event Loop
        window, event, values = sg.read_all_windows()

        if window == sg.WIN_CLOSED:     # if all windows were closed
            break

        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            # if closing win 2, mark as closed
            if window == list_of_window_references[1]:
                list_of_window_references[1] = None
            # if closing win 1, mark as closed
            elif window == list_of_window_references[0]:
                list_of_window_references[0] = None
        elif event == 'Next' or event == 'Prev':
            if event == 'Next':
                current_window += 1
                if current_window > max_windows - 1:
                    current_window = 0
            else:
                current_window -= 1
                if current_window < 0:
                    current_window = max_windows - 1
            show_current_window()
        elif event == 'Reopen':
            if not list_of_window_references[1]:
                list_of_window_references[1] = make_win2()
                list_of_window_references[1].move(list_of_window_references[0].current_location()[
                    0], list_of_window_references[0].current_location()[1] + 220)
        elif event == '-IN-':
            output_window = list_of_window_references[
                1] if window == list_of_window_references[0] else list_of_window_references[0]
            if output_window:           # if a valid window, then output to it
                output_window['-OUTPUT-'].update(values['-IN-'])
            else:
                window['-OUTPUT-'].update('Other window is closed')


if __name__ == '__main__':
    main()
