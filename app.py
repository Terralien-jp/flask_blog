from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter

from werkzeug.security import generate_password_hash, check_password_hash
import os

from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# worning出るので対策
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_maneger = LoginManager()
login_maneger.init_app(app)
bootstrap = Bootstrap(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(50))
    theme = db.Column(db.String(50))
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(20))
    
@login_maneger.user_loader
def lode_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
# @login_required
def index():
    if request.method == 'GET':
        posts = Post.query.all()
        # paginatoの設定、ページ内の投稿数を現在10としている
        page = request.args.get(get_page_parameter(), type=int, default=1)
        rows = posts[(page -1)*10: page*10]
        pagination = Pagination(page=page, total=len(posts), per_page=10, css_framework='bootstrap')
        return render_template('index.html', posts=posts, rows=rows, pagination=pagination)

# 記事ページ
@app.route('/article/<int:id>', methods=['GET'])
# @login_required
def article(id):
    post = Post.query.get(id)
    return render_template('article.html', post=post)

# signup,login,logout機能、今のところ有名無実
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User(username=username, password=generate_password_hash(password, method='sha256'))
        
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect('/login')

# 記事の新規作成
@app.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    if request.method == 'POST':
        genre = request.form.get('genre')
        theme = request.form.get('theme')
        title = request.form.get('title')
        body = request.form.get('body')
        
        post = Post(genre=genre, theme=theme, title=title, body=body)
        
        # 新規データなのでadd必要
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create.html')

# 記事の編集 createとほぼ同じ感じ
@app.route('/<int:id>/update', methods=['GET', 'POST'])
# @login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.genre = request.form.get('genre')
        post.theme = request.form.get('theme')
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        
        # すでにあるデータの編集なのでadd不要
        db.session.commit()
        return redirect('/')

# delete ページは作らずボタンで削除JSかなんかでダイアログ出した方がいい
@app.route('/<int:id>/delete', methods=['GET', 'POST'])
# @login_required
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect('/')