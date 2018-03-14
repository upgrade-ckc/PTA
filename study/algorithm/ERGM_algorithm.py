"""
    ERGM algorithm

"""

import pandas as pd
import numpy as np

ALPHA = 0.6180339887
BETA = 0.05


def cal_var(df, t):
    min = df[t].min()
    max = df[t].max()
    median = df[t].median()
    return min, max, median


def load_data(filename):
    df = pd.read_csv(filename)
    return df


def set_initial_values(df, t):
    min, max, median = cal_var(df, t)
    initial_density = df[t].count() / (max - min)
    threshold = median * BETA
    density_list = [0, ]
    return min, max, median, initial_density, threshold, density_list


def test(df, t):
    density_list = loop(df, t)
    optimal_k = determine_optimal_k(density_list)
    return optimal_k


def loop(df, t):
    min, max, median, initial_density, threshold, density_list = set_initial_values(df, t)
    cnt = 0
    print("Calculating ...")
    while True:
        cnt_l = sum(df[t] < median)
        cnt_r = sum(df[t] > median)
        len_l = median - min
        len_r = max - median

        density_l = cnt_l / len_l
        density_r = cnt_r / len_r

        if density_l < density_r:
            data = df[t][df[t].values < min + len_l * ALPHA]
        else:
            data = df[t][df[t].values > max - len_r * ALPHA]

        # drop noise point
        df = df.drop(data.keys())

        # calculate density
        density = df[t].count() / (max - min)
        density_list.append(abs(initial_density - density))
        cnt = cnt + 1
        print("min: ", min, "median: ", median, "max: ", max)
        min, max, median = cal_var(df, t)

        if (median - min) < threshold:
            print("median-min: ", median-min, "threshold", threshold)
            print("total loop count: ", cnt)
            print("Threshold breaking!\n")
            break
        elif (max - median) < threshold:
            print("max-median: ", median-min, "threshold", threshold)
            print("Loop count: ", cnt)
            print("Threshold breaking!\n")
            break

    return density_list


def main_loop(df, t, cnt):
    min, max, median, initial_density, threshold, density_list = set_initial_values(df, t)
    for x in range(0, cnt):
        print("================ ", (x+1), "th Main loop ===============================\n")
        cnt_l = sum(df[t] < median)
        cnt_r = sum(df[t] > median)
        len_l = median - min
        len_r = max - median

        density_l = cnt_l / len_l
        density_r = cnt_r / len_r

        if density_l < density_r:
            data = df[t][df[t].values < min + len_l * ALPHA]
        else:
            data = df[t][df[t].values > max - len_r * ALPHA]

        # drop noise point
        df = df.drop(data.keys())

        print("min: ", min, "median: ", median, "max: ", max, "\n")
        min, max, median = cal_var(df, t)

    print("================================================================\n")
    return df

def determine_optimal_k(density_list):
    # ( 0, 0 ) ~ ( len(density_list), density_list[len(density_list)-1] )
    #  y = mx (m is gradient) -> y-0 = (density_list[len(density_list)-1]/len(density_list))*x
    gradient = density_list[len(density_list) - 1] / (len(density_list) - 1)
    density_variation = []

    for x in range(len(density_list)):
        diff = abs(gradient * x - density_list[x])
        density_variation.append(diff)
    print("density list: ", density_list)
    print("density variation rate: ", density_variation)
    d_max = np.max(density_variation)
    # k - last iterations
    k = density_variation.index(d_max)
    print("d_max value: ", d_max)
    print("optimal k value: ", k, "\n")

    return k

def ERGM(filename, target):
    original_dataset = load_data(filename)

    ''' Test field '''
    # x가 0~24 까지 Hour field 를 filtering 해줌
    for x in [2]:
        test_dataset = original_dataset[original_dataset['Hour'] == x]
        # original_dataset = test_datasets
    ''' End test'''

    # sorted_dataset = original_dataset.sort_values(by=[target])
    sorted_dataset = test_dataset.sort_values(by=[target])

    # find optimal k
    k = test(sorted_dataset, target)
    final_data = main_loop(sorted_dataset, target, k)

    # target_data: 마지막에 graph로 뿌려줄 data // loop로 final_data append
    target_data = pd.DataFrame()
    target_data = target_data.append(final_data)

    import matplotlib.pyplot as plt

    # 원본 data
    plt.plot(original_dataset['Hour'], original_dataset[target], 'o', markersize=3)
    # 정리 data
    plt.plot(target_data['Hour'], target_data[target].values, 'o', color="orange", markersize=0.8)
    # label_name
    plt.xlabel('Hour')
    plt.ylabel(target)
    plt.show()








