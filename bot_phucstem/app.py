import os
import json
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

app = Flask(__name__)

# Load .env file
load_dotenv()

# File paths
sukien_path = os.path.join(os.getcwd(), os.getenv('SUKIEN'))
trucnhat_path = os.path.join(os.getcwd(), os.getenv('TRUCNHAT'))
baitapvenha_path = os.path.join(os.getcwd(), os.getenv('BTVN'))

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    """Trang chính hiển thị sự kiện"""
    events = load_json(sukien_path)
    return render_template('admin.html', events=events)

@app.route('/add_event', methods=['POST'])
def add_event():
    """Thêm sự kiện mới"""
    month = request.form['month']
    event = request.form['event']
    
    data = load_json(sukien_path)
    data[f"sukien{month}"] = event
    save_json(sukien_path, data)
    
    return redirect(url_for('index'))

@app.route('/delete_event', methods=['POST'])
def delete_event():
    """Xóa sự kiện"""
    month = request.form['month']
    
    data = load_json(sukien_path)
    if f"sukien{month}" in data:
        del data[f"sukien{month}"]
    save_json(sukien_path, data)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
