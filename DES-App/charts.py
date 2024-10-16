#Chart Module

#Import Statements for dependencies
import matplotlib.pyplot as plt
import numpy as np

class ChartManager:
    def __init__(self):
        pass

    #Draw Line Chart function
    def draw_line_chart(self):
        data_list = [-1, -4.5, 16, 23]
        plt.plot(data_list)
        plt.title("Line Chart Example")
        plt.xlabel("X Values")
        plt.ylabel("Y Values")
        return plt.gcf()
    
    #Draw Bar Chart function
    def draw_bar_chart(self):
        years = [str(year) for year in range(2010, 2019)]
        visitors = [1234, 5678, 8900, 345433, 22234, 55678, 43455, 76855, 69788]
        plt.bar(years, visitors, color="green")
        plt.xlabel("Year")
        plt.ylabel("Visitors")
        plt.title("Bar Chart Example")
        return plt.gcf()
    
    #Draw Scatter Plot Chart
    def draw_scatter_plot(self):
        x = np.random.rand(50) * 100
        y = np.random.rand(50) * 100
        colors = np.random.rand(50)
        sizes = (30 + np.random.rand(50)) ** 2

        plt.scatter(x, y, s=sizes, c=colors, alpha=0.8, edgecolor='k')

        plt.title("Scatter Plot Example")
        plt.xlabel("X Values")
        plt.ylabel("Y Values")
        plt.grid(True)
        return plt.gcf()
