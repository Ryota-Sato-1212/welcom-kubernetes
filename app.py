from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>波の動画背景</title>
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
                font-family: sans-serif;
            }

            .video-background {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                object-fit: cover;
                z-index: -1;
            }

            .content {
                position: relative;
                z-index: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100%;
                color: white;
                text-shadow: 1px 1px 4px #000;
            }

            button {
                padding: 15px 30px;
                font-size: 18px;
                background-color: rgba(255, 255, 255, 0.8);
                border: none;
                border-radius: 10px;
                cursor: pointer;
                transition: 0.3s;
            }

            button:hover {
                background-color: white;
            }
        </style>
    </head>
    <body>
        <video class="video-background" autoplay muted loop>
            <source src="{{ url_for('static', filename='video/wave.mp4') }}" type="video/mp4">
        </video>

        <div class="content">
            <h1>ようこそ、Kubernetesの世界へ</h1>
            <button onclick="window.open('https://kubernetes.io/ja/', '_blank')">kubernetes</button>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)