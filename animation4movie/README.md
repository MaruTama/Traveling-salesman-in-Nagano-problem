コードやd3.js、TopoJSONの説明
- [TopoJSON v2, v3の使い方 -コマンドライン編-](https://qiita.com/cieloazul310/items/6dfd73952304ab61cd20)
- [D3.jsでWebに地図を描く【TopoJSON作成・Toposimplify圧縮比較】](https://ssit.jp/d3-map-diff-toposimplify/)
- [d3.js "v4" にて地図描画](https://qiita.com/hiyuzawa/items/b28fa4d380d02d8bd5a1)

データダウンロード
- [国土数値情報　行政区域データ](http://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-N03-v2_3.html)

GeoJSONやshpの説明
- [D3.jsで地図を描画](https://www.excellence-blog.com/2018/04/06/d3-js%E3%81%A7%E5%9C%B0%E5%9B%B3%E3%82%92%E6%8F%8F%E7%94%BB/)


市町村のマッピング
```
$ unzip N03-190101_20_GML.zip
$ brew install node
$ npm install -g topojson shapefile
$ cd animation4movie
#shpファイルからtopojsonに変換(shapefile)
$ shp2json --encoding "Shift-JIS" N03-190101_20_GML/N03-19_20_190101.shp | geo2topo -q 1e6 > output.topojson
#TopoJSONのデータサイズを縮小する(topojson)
$ toposimplify -P 0.1 output.topojson > pref.Nagano.json
$ rm output.topojson
```

経路
kml -> TopoJSON
https://mapbox.github.io/togeojson/ でも変換できる
```
$ npm install -g @mapbox/togeojson
$ togeojson 焼きまんじゅうマップ.kml > 焼きまんじゅうマップ.geojson
```


ローカルでファイルを読み込むとエラーになるので、適当にサーバーを立てる
```
npm install -g http-server
http-server
Goto http://localhost:8080/
```
