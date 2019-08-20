
# [Google Map Directions API で日本国内の路線検索はできない](https://qiita.com/seigo-pon/items/bff784040e9e46dc8a56)
# [巡回セールスマン問題](http://codecrafthouse.jp/p/2016/08/traveling-salesman-problem/)
# [「巡回セールスマン問題」を解くアルゴリズムを可視化したムービー](https://gigazine.net/news/20160512-traveling-salesman-problem-visualization/)
# [巡回セールスマン問題から始まる数理最適化](https://qiita.com/panchovie/items/6509fb54e3d53f4766aa)
# [2.12 巡回セールスマン問題](http://www.msi.co.jp/nuopt/docs/v19/examples/html/02-12-00.html)
# [巡回セールスマン問題を2-opt法で解く（Python）](https://kanchi0914.hatenablog.com/entry/2018/06/13/181330)
#
# python nagano.py [GOOGLE_MAP_API_KEY] ./nagano.json


'''
長野市 -> 千曲市 -> 坂城町 -> 麻績村 -> 筑北村 -> 青木村 -> 上田市 -> 長和町 -> 立科町 ->
東御市 -> 小諸市 -> 御代田町 -> 軽井沢町 -> 佐久市 -> 佐久穂町 -> 小海町 -> 北相木村 ->
南相木村 -> 川上村 -> 南牧村 -> 富士見町 -> 原村 -> 茅野市 -> 諏訪市 -> 下諏訪町 ->
岡谷市 -> 辰野町 -> 箕輪町 -> 南箕輪村 -> 伊那市 -> 宮田村 -> 駒ヶ根市 -> 飯島町 ->
中川村 -> 大鹿村 -> 松川町 -> 高森町 -> 豊丘村 -> 喬木村 -> 飯田市 -> 下條村 -> 泰阜村 ->
阿南町 -> 天龍村 -> 売木村 -> 平谷村 -> 根羽村 -> 阿智村 -> 南木曽町 -> 大桑村 -> 上松町 ->
王滝村 -> 木曽町 -> 木祖村 -> 塩尻市 -> 朝日村 -> 山形村 -> 松本市 -> 安曇野市 -> 松川村 ->
池田町 -> 生坂村 -> 大町市 -> 白馬村 -> 小谷村 -> 小川村 -> 信濃町 -> 飯綱町 -> 飯山市 ->
木島平村 -> 栄村 -> 野沢温泉村 -> 山ノ内町 -> 中野市 -> 小布施町 -> 高山村 -> 須坂市 ->
多スタート戦略で得られた経路の総移動距離 = 1304.8 km
'''


import numpy as np
import matplotlib.pyplot as plt
import math
import json
import directionsAPI as da
import sys
import argparse

plt.style.use('ggplot')



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


# 長野県各市町村間距離算出
# 時間掛かる 15分くらい
def getMunicipalitiesDirection(city_xy, api_key):
    # 都市間距離を計算
    NUM = len(city_xy)
    list_dis = [[0 for i in range(NUM)] for j in range(NUM)]
    list_tim = [[0 for i in range(NUM)] for j in range(NUM)]

    for i in range(NUM-1):
        for j in range(NUM-i-1):
            src = da.MapCoordinate(float(city_xy[i][0]), float(city_xy[i][1])) # 出発地
            dest = da.MapCoordinate(float(city_xy[j+i+1][0]), float(city_xy[j+i+1][1])) # 目的地
            route = da.MapRoute(src, dest, da.MapRoute.mode_driving)
            direction_json = da.getGoogleMapDirection(route, api_key)
            #所要時間を取得
            for key in direction_json['routes']:
                for key2 in key['legs']:
                    print(key2['distance']['text']) # 距離
                    print(key2['duration']['text']) # 所要時間
                    # "XX.X km" となってるので数値のみにする
                    list_dis[i][j+i+1] = float(key2['distance']['text'][:-3])
                    list_dis[j+i+1][i] = float(key2['distance']['text'][:-3])
                    list_tim[i][j+i+1] = key2['duration']['text']
                    list_tim[j+i+1][i] = key2['duration']['text']


    # json 読み出し
    f = open(NAGANO_JSON, 'r')
    json_data = json.load(f)

    # json 書き出し
    f = open(NAGANO_JSON, "w")
    json_data.update( {"Distance_matrix": list_dis} )
    json_data.update( {"Time_matrix": list_tim} )
    json.dump(json_data, f, ensure_ascii=False, indent=2, sort_keys=True, separators=(',', ': '))


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="長野県の各市町村間を巡る市町村順序")
    parser.add_argument(
        "api_key", metavar="GOOGLE_MAP_API_KEY", help="Goolge Map Direction API Token")
    parser.add_argument(
        "naganoe_json", metavar="nagano.json", help="Prof.Ngano's Municipalities json fileneme")
    return parser.parse_args(args)

def main(args=None):

    options = parse_args(args)
    api_key = options.api_key
    NAGANO_JSON = options.naganoe_json

    # jsonから緯度経度を取り出す
    f = open(NAGANO_JSON, 'r')
    dict_nagano = json.load(f)

    # 緯度経度を取り出して ndarray に変換する
    # 順序は自治体コード順で取り出す
    municipalities = dict_nagano["Municipalities"]
    city_xy = np.array([municipalities[m]["LL"] for m in dict_nagano["Code_asc"]])
    NUM = len(city_xy)

    # 長野県各市町村間距離算出
    # 時間掛かるし、使いすぎるとお金掛かるから、json に記録する
    # getMunicipalitiesDirection(city_xy, api_key)
    # json 読み出し
    # f = open(NAGANO_JSON, 'r')
    # dict_nagano = json.load(f)

    # 長野県各市町村間距離の取り出し
    distance_matrix = np.array(dict_nagano["Distance_matrix"])
    # distance_matrix[i, j]が都市iと都市jの距離。
    print(np.round(distance_matrix[:10, :10]))
    print()

    # 都市を表示
    # print(city_xy)
    plt.figure(figsize=(4, 4))
    plt.plot(city_xy[:, 0], city_xy[:, 1], 'o')
    plt.show()


    # 試しに距離を計算してみる
    # 経路をランダムに選択
    test_order = list(np.random.permutation(NUM))
    print('ランダム訪問順序 = {}'.format(test_order))
    total = calculate_total_distance(test_order, distance_matrix)
    print('ランダム総移動距離 = {:.1f} km'.format(total))
    print()


    # 多スタート戦略
    N_START = 200
    order_best = None
    score_best = sys.float_info.max

    for _ in range(N_START):
        order_random = list(np.random.permutation(NUM))
        order_improved = local_search(
            order_random, distance_matrix, improve_with_2opt)
        score = calculate_total_distance(order_improved, distance_matrix)

        if score < score_best:
            score_best = score
            order_best = order_improved

    total_distance = calculate_total_distance(order_best, distance_matrix)
    # print('多スタート戦略で得られた経路の訪問順序 = {}'.format(order_best))
    print("市町村経路")
    for i in order_best:
        print("{} -> ".format(dict_nagano["Code_asc"][i]), end='')
    print("最初へ")
    print('多スタート戦略で得られた経路の総移動距離 = {:.1f} km'.format(total_distance))
    # 経路を可視化する
    visualize_visit_order(order_best, city_xy)


if __name__ == '__main__':
    sys.exit(main())
