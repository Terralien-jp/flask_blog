# flask_blog
CRUD操作を備えたblog

## step2 create a blog

https://www.youtube.com/watch?v=VtJ-fGm4gNg

### 使用ライブラリ等
flask_sqlalchemy
sqlite3

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