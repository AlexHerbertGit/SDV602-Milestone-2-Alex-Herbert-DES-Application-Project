"""Chart/Graph Creation and Settings Module"""

"""Import Statements for dependencies"""
import matplotlib.pyplot as plt
import numpy as np

"""ChartManager Class"""
class ChartManager:
    def __init__(self):
        pass

    def draw_line_chart(self, data=None):
        """Draws a line chart with provided data."""
        plt.figure()
        if data is not None:
            x = data.iloc[:, 0]  # First column as X-axis
            y = data.iloc[:, 1]  # Second column as Y-axis
            plt.plot(x, y, marker="o", linestyle="-")
            plt.title("Line Chart")
            plt.xlabel("X Axis")
            plt.ylabel("Y Axis")
        else:
            plt.text(0.5, 0.5, "No Data", ha="center", va="center", fontsize=12)
        return plt.gcf()

    def draw_bar_chart(self, data=None):
        """Draws a bar chart with provided data."""
        plt.figure()
        if data is not None:
            x = data.iloc[:, 0]  # First column as categories
            y = data.iloc[:, 1]  # Second column as values
            plt.bar(x, y, color="skyblue")
            plt.title("Bar Chart")
            plt.xlabel("Categories")
            plt.ylabel("Values")
        else:
            plt.text(0.5, 0.5, "No Data", ha="center", va="center", fontsize=12)
        return plt.gcf()

    def draw_scatter_plot(self, data=None):
        """Draws a scatter plot with provided data."""
        plt.figure()
        if data is not None:
            x = data.iloc[:, 0]  # First column as X-axis
            y = data.iloc[:, 1]  # Second column as Y-axis
            plt.scatter(x, y, c="red", alpha=0.5)
            plt.title("Scatter Plot")
            plt.xlabel("X Axis")
            plt.ylabel("Y Axis")
        else:
            plt.text(0.5, 0.5, "No Data", ha="center", va="center", fontsize=12)
        return plt.gcf()
