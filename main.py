from genetic import *
from parameter import *
import os
import matplotlib.pyplot as chart

while True:
    os.system('cls')

    param = input_parameter()
    param.input()

    iteration, fitness_chart, weight_chart = genetic(param)

    chart.plot(iteration, fitness_chart)
    chart.plot(iteration, weight_chart)
    chart.show()