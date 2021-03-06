
# 導入
市町村のマッピングを行う。  
geojson は緯度経度をもち絶対値、topojson は相対値であり位置情報を持たないが軽量である。  
今回は、経路データも表示したいので緯度経度情報を保持する GeoJson のほうが好ましい。

## 市町村形状データの取得
```
$ unzip N03-190101_20_GML.zip
$ brew install node
$ npm install -g topojson shapefile
$ cd animation4movie
#shpファイルからGeoJsonに変換(shapefile)
$ shp2json --encoding "Shift-JIS" N03-190101_20_GML/N03-19_20_190101.shp > pref.Nagano.geojson

#今回未使用(TopoJsonをつかうとき)
#shpファイルからtopojsonに変換(shapefile)
$ shp2json --encoding "Shift-JIS" N03-190101_20_GML/N03-19_20_190101.shp | geo2topo -q 1e6 > output.topojson
#TopoJSONのデータサイズを縮小する(topojson)
$ toposimplify -P 0.1 output.topojson > pref.Nagano.topojson
$ rm output.topojson
```
## 各市町村間の経路データの取得

kml -> GeoJSON に変換する  
マイマップを作ってダウンロードしたもの  
セクション（役場間の経路）ごとで分けたファイルをつくる。  
しかし、マイマップだとレイヤを10個しか作れないので手動で結合する。  
Folder タグが各セクション

```
$ npm install -g @mapbox/togeojson
$ togeojson history-route.kml > history-route.geojson
```

# 使い方
ローカルでファイルを読み込むとエラーになるので、適当にサーバーを立てる
```
npm install -g http-server
http-server
Goto http://localhost:8080/
```


# ref
コードやd3.js、TopoJSONの説明

- [TopoJSON v2, v3の使い方 -コマンドライン編-](https://qiita.com/cieloazul310/items/6dfd73952304ab61cd20)
- [【D3.js】地図上に都市と都市を結ぶ線を引く](https://shimz.me/blog/d3-js/2913)
- [D3.jsでWebに地図を描く【TopoJSON作成・Toposimplify圧縮比較】](https://ssit.jp/d3-map-diff-toposimplify/)
- [d3.js "v4" にて地図描画](https://qiita.com/hiyuzawa/items/b28fa4d380d02d8bd5a1)
- [D3.jsで都道府県別の地図を描く](https://qiita.com/ran/items/d88c5126362576be3291)
- [【D3.js】複数のデータファイルの読み込み(非同期処理)をまとめる](https://shimz.me/blog/d3-js/3087)

データダウンロード

- [国土数値情報　行政区域データ](http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html)

GeoJSONやshpの説明

- [D3.jsで地図を描画](https://www.excellence-blog.com/2018/04/06/d3-js%E3%81%A7%E5%9C%B0%E5%9B%B3%E3%82%92%E6%8F%8F%E7%94%BB/)
- [D3.jsで日本地図を描くときの基本(geojson)](https://qiita.com/sand/items/422d4fab77ea8f69dfdf)

アニメーション

- [D3.js v4/v5 アニメ―ション使い方 エフェクト一覧(transition, ease)](https://wizardace.com/d3-transition-ease/)
- [【D3.js】 地図上のルートに沿ってアニメーション](https://shimz.me/blog/d3-js/2993)
