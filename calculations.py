import math
def count_average(numbers, amount_of_num):
    return round((sum(numbers)/amount_of_num), 2)


def count_deviation(number, average, amount_of_num):
    return round(math.sqrt(sum((number - average)**2)/amount_of_num), 4)