import numpy as np
import matplotlib.pyplot as plt
import calculations
import easygui
import pathlib

def get_data(filename):
    try:
        with open(f"{filename}.csv", encoding='utf-8-sig') as fopen:
            content = fopen.read()
            return content
    except FileNotFoundError:
        print(f'File {filename} was not found. ')

def show_bar(x_axis, y_axis, filename):
    plt.xticks(size=7, rotation=30)
    plt.bar(x_axis, y_axis, label=f'Hardness for {filename}', width=120, color='b')
    plt.title('The hardness of the weld in relation to the distance from its center')
    plt.legend()
    plt.xlabel('The distance from the center of the weld [µm]')
    plt.ylabel('Hardness [HV]')
    plt.savefig(f'BarPlot_{filename}.pdf')
    plt.show()

def show_scatter(x_axis, y_axis, filename):
    plt.scatter(x_axis, y_axis, label=f'Hardness for {filename}', color='purple', s=30, alpha=0.8)
    plt.title('The hardness of the weld in relation to the distance from its center')
    plt.legend()
    plt.xlabel('The distance from the center of the weld [µm]')
    plt.ylabel('Hardness [HV]')
    plt.savefig(f'ScatterPlot_{filename}.pdf')
    plt.show()

def show_line(x_axis, y_axis, filename):
    plt.plot(x_axis, y_axis, ls='-', label=f'Hardness for {filename}', linewidth='1.5', c='g', marker='.', ms=6)
    plt.title('The hardness of the weld in relation to the distance from its center')
    plt.legend()
    plt.xlabel('The distance from the center of the weld [µm]')
    plt.ylabel('Hardness [HV]')
    plt.savefig(f'LinePlot_{filename}.pdf')
    plt.show()

def build_graph(graph_type, filename, hardness, position, ar_position):
    if len(graph_type) != 1:
        print('You entered too long name. I do not understand. Please repeat. ')
    elif graph_type == 'b':
        show_bar(ar_position, hardness, filename)
    elif graph_type == 's':
        show_scatter(position, hardness, filename)
    else:
        show_line(position, hardness, filename)

def prepare_data(filename):
    user_data = get_data(filename).replace('\n', ';').replace(' ', '').replace(',', '.').split(';')
    int_user_data = np.array(user_data, dtype=float)
    reshaped_data = int_user_data.reshape(-1, 3)
    final_data = np.stack((reshaped_data[0:]), axis=1)
    hardness = final_data[1]  # measured_hardness
    for val in hardness:
        if val < 0:
            raise ValueError
    position = final_data[2]  # position_of_measurement
    str_position = position.copy()
    str_position.astype(str)
    return hardness, position, str_position

def main():
    filename = easygui.fileopenbox(filetypes=['*.csv'], default='*.csv')
    filename = pathlib.Path(filename).name.replace('.csv', '')

    graph_type = input('Pick the type of graph you want to receive: bar(b), scatter(s) or line(l): ')
    hardness, position, str_position = prepare_data(filename)

    average = calculations.count_average(hardness, len(hardness))
    deviation = calculations.count_deviation(hardness, average, len(hardness))
    print(f'For this data the average hardness is {average} HV whereas the standard deviation is {deviation}.')

    build_graph(graph_type, filename, hardness, position, str_position)


if __name__ == '__main__':
    main()
