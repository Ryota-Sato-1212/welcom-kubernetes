from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/blog")
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.asc()).all()
    return render_template("blog.html", posts=posts)

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

@app.route("/blog/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("blog"))
    return render_template("edit_post.html", post=post)

@app.route("/blog/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog"))

@app.route("/blog/<int:post_id>")
def post_detail(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template("post_detail.html", post=post)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form["query"]
        prompt = f"「{query}」について簡単に説明してください。"

        result = ""
        try:
            client = OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            result = response.choices[0].message.content

        except OpenAIError as e:
            print("OpenAI API call failed:", e)
            result = f"（ダミー応答）「{query}」に関する情報は現在取得できませんが、通常はここにAIの回答が表示されます。"

        return render_template("search_results.html", query=query, result=result)

    return render_template("search_form.html")

if __name__ == "__main__":
    app.run(debug=True, port=5050)