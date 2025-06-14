from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import openai
import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# OpenAI APIキー設定（セキュリティ上 .env に入れるのが望ましい）
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY is not set in the environment or .env file")
openai.api_key = openai_api_key

# データベース設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# モデル定義
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# データベース初期化
with app.app_context():
    db.create_all()

# ホームページ
@app.route("/")
def home():
    return render_template("index.html")

# ブログ記事一覧
@app.route("/blog")
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.asc()).all()
    return render_template("blog.html", posts=posts)

# 新規投稿
@app.route("/blog/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = BlogPost(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("blog"))
    return render_template("new_post.html")

# 記事編集
@app.route("/blog/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("blog"))
    return render_template("edit_post.html", post=post)

# 記事削除
@app.route("/blog/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog"))

# 記事詳細
@app.route("/blog/<int:post_id>")
def post_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

# AI検索機能
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"]

        prompt = f"「{query}」について簡単に説明してください。"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            result = response.choices[0].message["content"]
            print("OpenAI response:", result)  # 動作確認用
        except Exception as e:
            print("OpenAI API call failed:", e)
            result = f"エラーが発生しました: {e}"

        return render_template("search_results.html", query=query, result=result)

    return render_template("search_form.html")
# アプリ起動
if __name__ == "__main__":
    app.run(debug=True, port=5050)