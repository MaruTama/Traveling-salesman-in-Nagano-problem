
# [巡回セールスマン問題](http://codecrafthouse.jp/p/2016/08/traveling-salesman-problem/)
import numpy as np
import matplotlib.pyplot as plt
import math
import sys

plt.style.use('ggplot')

N = 80
MAP_SIZE = 100


# 総移動距離の計算をする関数
# 訪問順の評価指標
def calculate_total_distance(order, distance_matrix):
    """Calculate total distance traveled for given visit order"""
    idx_from = np.array(order)
    idx_to = np.array(order[1:] + [order[0]])
    distance_arr = distance_matrix[idx_from, idx_to]

    return np.sum(distance_arr)

# 訪問経路の可視化
def visualize_visit_order(order, city_xy):
    """Visualize traveling path for given visit order"""
    route = np.array(order + [order[0]])  # add point of departure
    x_arr = city_xy[:, 0][route]
    y_arr = city_xy[:, 1][route]

    plt.figure(figsize=(4, 4))
    plt.plot(x_arr, y_arr, 'o-')
    plt.show()

# 交換による総移動距離の差分を計算する関数
def calculate_2opt_exchange_cost(visit_order, i, j, distance_matrix):
    """Calculate the difference of cost by applying given 2-opt exchange"""
    n_cities = len(visit_order)
    a, b = visit_order[i], visit_order[(i + 1) % n_cities]
    c, d = visit_order[j], visit_order[(j + 1) % n_cities]

    cost_before = distance_matrix[a, b] + distance_matrix[c, d]
    cost_after = distance_matrix[a, c] + distance_matrix[b, d]
    return cost_after - cost_before

# ２つのパスの交換後の訪問順序を計算する
def apply_2opt_exchange(visit_order, i, j):
    """Apply 2-opt exhanging on visit order"""

    tmp = visit_order[i + 1: j + 1]
    tmp.reverse()
    visit_order[i + 1: j + 1] = tmp

    return visit_order

# 2-optによる近傍探索
def improve_with_2opt(visit_order, distance_matrix):
    """Check all 2-opt neighbors and improve the visit order"""
    n_cities = len(visit_order)
    cost_diff_best = 0.0
    i_best, j_best = None, None

    for i in range(0, n_cities - 2):
        for j in range(i + 2, n_cities):
            if i == 0 and j == n_cities - 1:
                continue

            cost_diff = calculate_2opt_exchange_cost(
                visit_order, i, j, distance_matrix)

            if cost_diff < cost_diff_best:
                cost_diff_best = cost_diff
                i_best, j_best = i, j

    if cost_diff_best < 0.0:
        visit_order_new = apply_2opt_exchange(visit_order, i_best, j_best)
        return visit_order_new
    else:
        return None

def local_search(visit_order, distance_matrix, improve_func):
    """Main procedure of local search"""
    cost_total = calculate_total_distance(visit_order, distance_matrix)

    while True:
        improved = improve_func(visit_order, distance_matrix)
        if not improved:
            break

        visit_order = improved

    return visit_order

def main():

    # 都市を表示
    np.random.seed(10)
    city_xy = np.random.rand(N, 2) * MAP_SIZE
    plt.figure(figsize=(4, 4))
    plt.plot(city_xy[:, 0], city_xy[:, 1], 'o')
    plt.show()

    x = city_xy[:, 0]
    y = city_xy[:, 1]
    # 都市間距離を計算
    distance_matrix = np.sqrt((x[:, np.newaxis] - x[np.newaxis, :]) ** 2 +
                              (y[:, np.newaxis] - y[np.newaxis, :]) ** 2)

    # 見やすくするために10都市分だけ出力。
    # distance_matrix[i, j]が都市iと都市jの距離。
    print(np.round(distance_matrix[:10, :10]))


    # 試しに距離を計算してみる
    test_order = list(np.random.permutation(N))
    print('訪問順序 = {}'.format(test_order))

    total = calculate_total_distance(test_order, distance_matrix)
    print('総移動距離 = {}'.format(total))

    # 可視化を試してみる
    # visualize_visit_order(test_order, city_xy)


    # 多スタート戦略
    N_START = 100
    order_best = None
    score_best = sys.float_info.max

    for _ in range(N_START):
        order_random = list(np.random.permutation(N))
        order_improved = local_search(
            order_random, distance_matrix, improve_with_2opt)
        score = calculate_total_distance(order_improved, distance_matrix)

        if score < score_best:
            score_best = score
            order_best = order_improved

    # 可視化を試してみる
    visualize_visit_order(order_best, city_xy)
    total_distance = calculate_total_distance(order_best, distance_matrix)
    print('多スタート戦略で得られた経路の総移動距離 = {}'.format(total_distance))

if __name__ == '__main__':
    main()
