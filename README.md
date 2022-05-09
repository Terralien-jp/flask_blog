# flask_blog
CRUD操作を備えたblog

## 全完了

https://www.youtube.com/watch?v=VtJ-fGm4gNg

### 課題
* ユーザー重複
* bootstrapの適用
    * 別のフロントエンドによる解決法はないか？
* 各例外処理
* ログインしてない場合ログイン画面を表示

### 使用ライブラリ等
flask_sqlalchemy
flask-login
sqlite3
bootstrap5

## 起動方法

`FLASK_APP=app.py FLASK_ENV=development flask run`

### 環境変数の指定
```bash
export FLASK_APP=app.py
# 開発時使用、高速リロードなど便利
export FLASK_ENV=development
# 別のアプリ作ったときなど環境変数を変えてしまってることがあるので確認
printenv FLASK_APP
```

環境変数を指定以降は`flask run`のみで実行できる。