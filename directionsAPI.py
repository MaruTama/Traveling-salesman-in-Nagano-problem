
# [Google Map Directions API で日本国内の路線検索はできない](https://qiita.com/seigo-pon/items/bff784040e9e46dc8a56)
# python directionsAPI.py GOOGLE_MAP_API_KEY ./nagano.json

import urllib.request
import json
import os
import sys
import argparse

# 位置座標クラス
class MapCoordinate:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def position(self):
        return "{0},{1}".format(self.latitude, self.longitude)

# ルートクラス
class MapRoute:
    mode_driving = "driving"

    def __init__(self, src, dest, mode):
        self.src = src
        self.dest = dest
        self.mode = mode
        self.lang = "ja"
        self.units = "metric"
        self.region = "ja"

# Goolge Map Direction 取得
def getGoogleMapDirection(route, api_key):

    # Google Maps Direction API URL
    url = "https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&mode={2}&language={3}&units={4}&region={5}&key={6}"

    try:
        # GET通信
        api_url = url.format(
            route.src.position(),
            route.dest.position(),
            route.mode,
            route.lang,
            route.units,
            route.region,
            api_key)

        print('')
        print('=====')
        print('url')
        print(api_url)
        print('=====')

        html = urllib.request.urlopen(api_url)

        html_json = json.loads(html.read().decode('utf-8'))
        return html_json

    except Exception as e:
        raise e

def parse_args(args):
    parser = argparse.ArgumentParser(
        description="長野県の各市町村間の時間・距離を算出する")
    parser.add_argument(
        "api_key", metavar="GOOGLE_MAP_API_KEY", help="Goolge Map Direction API Token")
    return parser.parse_args(args)

def main(args=None):

    options = parse_args(args)
    api_key = options.api_key

    src = MapCoordinate(34.733165, 135.500214) # 新大阪駅
    dest = MapCoordinate(34.686669, 135.519586) # 大阪府庁舎
    route = MapRoute(src, dest, MapRoute.mode_driving)

    direction_json = getGoogleMapDirection(route, api_key)

    #所要時間を取得
    for key in direction_json['routes']:
        #print(key) # titleのみ参照
        #print(key['legs'])
        for key2 in key['legs']:
            print('')
            print('=====')
            print(key2['distance']['text'])
            print(key2['duration']['text'])
            print('=====')

if __name__ == '__main__':
    sys.exit(main())
