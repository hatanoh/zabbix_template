# zabbix_template
作成した諸諸のzabbix templateをまとめてあります。
## ファイル
- template_nature_remo.xml  
 NatureRemoデータ取得用テンプレート
- template_switchbot.xml  
 switchbotデータ取得用テンプレート
- switchbot_api_helper.py  
 switchbotAPI取得用ヘルパースクリプト。  
 zbx_env/usr/lib/zabbix/externalscriptsに置きます。  
 使用にはpythonとpy-requestsが必要です。  
 標準のdocker compose (docker-compose_v3_alpine_pgsql_latest.yaml) を使用した場合どちらも入っていませんので、Dockerfileに追記してlocal.yamlの方でupするとよいかと思います。

## NatureRemo
### 対象デバイス
NatureRemo及びNatureRemo E liteのデータを取得します。
- NatureRemo

|センサ|更新間隔|
|-|-|
|温湿度センサー|1m|
|照度センサー|1m|
|人感センサー|1m|
- NatureRemo E lite

|センサ|更新間隔|
|-|-|
|瞬間消費電力|1m|
|累積消費電力|30m/1d|
### 使い方
1. インポートして適当なホストにテンプレートとして設定。
1. マクロACCESS_TOKENにNature Remo Cloud APIのアクセストークンを設定します。 アクセストークンはhome.nature.globalから取得してください(扱いは慎重に)
1. (オプション)マクロDEVICENAME.*を設定して取得するセンサを指定します。デフォルトでは見つかったすべてのRemoとRemo E liteのデータを取得します。
### API発行間隔
Remoはいくつあった場合でも1mにAPI1回リクエストします。Remo E liteは1つにつきAPIを1回リクエストします。  
通常1mに2回APIリクエストします。それに加え累積消費電力取得のため30minに1回/1dに1回、ディスカバリのため1hに2回のリクエストを行います。  
APIリクエスト間隔が気になる場合はnr.appliance[{#NAME}]/nr.device[{#NAME}]の更新間隔を調整してください。
### マクロ
|マクロ名|既定値|説明|
|-|-|-|
|{$ACCESS_TOKEN}|なし|アクセストークン|
|{$DEVICENAME.MATCHES}|.+|このマクロにマッチした名前のセンサーのデータを取得します|
|{$DEVICENAME.NOMATCHES}|0^|このマクロにマッチした名前のセンサーのデータは取得しません|

## SwitchBot
### 対象デバイス
Switchbot社製の温湿度計、温湿度計プラス、防水温湿度計。及びプラグミニ、K20+クリーナーのデータを収集します。
- 温湿度計、温湿度計プラス、防水温湿度計
  
|センサ|更新間隔|
|-|-|
|温湿度センサー|5m|
|照度センサー|5m|
|バッテリ|5m|
- プラグミニ
  
|センサ|更新間隔|
|-|-|
|電流|5m|
|消費電力|5m|
|ON/OFF|5m|
|使用時間|5m|
|電圧|5m|
- K20+クリーナー
  
|センサ|更新間隔|
|-|-|
|バッテリ|5m|
|状態|5m|
### 使い方
1. /usr/lib/zabbix/externalscripts にswitchbot_api_helper.pyを置き、実行可能にしておきます。
1. インポートして適当なホストにテンプレートとして設定。
1. マクロAUTHORIZATION及びCLIENT_SECRETにトークンとクライアントシークレットを設定します。switchbotアプリの開発者向けオプションから取得してください。
1. (オプション)マクロDEVICENAME.*を設定して取得するデバイスを指定する。デフォルトでは見つかったすべての対象デバイスのデータを取得します。
### API発行間隔
デバイスごとにAPIを1回発行します。また、ディスカバリのため1hに3回のリクエストを行います。  
標準では5分ごとにしてあり30台程度のデバイスを扱うことができますので通常のご家庭では問題ありません。  
それ以上のデバイスがある場合は間隔をあけるか、DEVICENAME.*マクロで取得するデバイスを絞ってください。  
更新間隔を上げる場合はAPI発行制限に注意して上げてください。
### マクロ
|マクロ名|既定値|説明|
|-|-|-|
|{$AUTHORIZATION}|なし|トークン|
|{$CLIENT_SECRET}|なし|クライアントシークレット|
|{$DEVICENAME.MATCHES}|.+|このマクロにマッチした名前のセンサーのデータを取得します|
|{$DEVICENAME.NOMATCHES}|0^|このマクロにマッチした名前のセンサーのデータは取得しません|
