from flask import Flask

app = Flask(__name__)

count = 0
@app.route('/')
def main_page():
    global count
    count += 1
    return f'Количество посетителей: {count}'
