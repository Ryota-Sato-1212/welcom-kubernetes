from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import sqlite3
import subprocess
import json

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='todo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

with app.app_context():
    db.drop_all()
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

@app.route("/tasks")
def tasks():
    try:
        tasks = Task.query.all()
        tasks_json = [task.to_dict() for task in tasks]
        return render_template("tasks.html", tasks=tasks_json)
    except Exception as e:
        app.logger.error(f"Error in tasks route: {str(e)}")
        return render_template("tasks.html", tasks=[])

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        app.logger.error(f"Error getting tasks: {str(e)}")
        return jsonify({'error': 'Failed to get tasks'}), 500

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            status='todo'
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        app.logger.error(f"Error creating task: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create task'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        return jsonify(task.to_dict())
    except Exception as e:
        app.logger.error(f"Error getting task {task_id}: {str(e)}")
        return jsonify({'error': 'Failed to get task'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        app.logger.error(f"Error updating task {task_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update task'}), 500

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        app.logger.error(f"Error deleting task {task_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete task'}), 500

@app.route('/api/tasks/<int:task_id>/status', methods=['POST'])
def update_task_status(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        app.logger.error(f"Error updating task status {task_id}: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update task status'}), 500

@app.route("/wiki")
def wiki():
    return render_template("wiki.html")

@app.route("/k8s_exercise")
def k8s_exercise():
    return render_template("k8s_exercise.html")

@app.route("/k8s_exercise/execute", methods=["POST"])
def execute_k8s_command():
    try:
        data = request.get_json()
        command = data.get("command", "")
        
        if not command:
            return jsonify({"error": "No command provided"}), 400
            
        # コマンドを実行
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return jsonify({
                "error": "Command execution failed",
                "output": result.stderr
            }), 400
            
        return jsonify({
            "output": result.stdout,
            "error": None
        })
        
    except Exception as e:
        app.logger.error(f"Error executing command: {str(e)}")
        return jsonify({
            "error": f"Failed to execute command: {str(e)}",
            "output": None
        }), 500

@app.route("/k8s_exercise/status", methods=["GET"])
def get_minikube_status():
    try:
        result = subprocess.run(
            ["minikube", "status"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return jsonify({
                "status": "error",
                "message": "Failed to get Minikube status",
                "details": result.stderr
            }), 500
            
        return jsonify({
            "status": "success",
            "message": result.stdout
        })
        
    except Exception as e:
        app.logger.error(f"Error getting Minikube status: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Failed to get Minikube status: {str(e)}"
        }), 500

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # サンプルタスクの追加
        sample_tasks = [
            {
                'title': 'Kubernetes Basics',
                'description': 'Learn fundamental concepts of Kubernetes including pods, services, and deployments',
                'status': 'todo'
            },
            {
                'title': 'Pod Management',
                'description': 'Understanding pod lifecycle, health checks, and resource management',
                'status': 'todo'
            },
            {
                'title': 'Service Discovery',
                'description': 'Learn about different types of services and service discovery mechanisms',
                'status': 'todo'
            },
            {
                'title': 'ConfigMaps and Secrets',
                'description': 'Managing configuration and sensitive data in Kubernetes',
                'status': 'todo'
            },
            {
                'title': 'Stateful Applications',
                'description': 'Deploying and managing stateful applications using StatefulSets',
                'status': 'todo'
            },
            {
                'title': 'Advanced Networking',
                'description': 'Understanding Kubernetes networking concepts and policies',
                'status': 'todo'
            },
            {
                'title': 'Security Best Practices',
                'description': 'Implementing security measures and best practices in Kubernetes',
                'status': 'todo'
            }
        ]
        
        for task_data in sample_tasks:
            task = Task(**task_data)
            db.session.add(task)
        
        db.session.commit()

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5051)