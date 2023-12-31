from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# データベースに接続

def connect_db():
    return psycopg2.connect(os.environ['DATABASE_URL'])


# ユーザーデータベースの作成
def create_user_table():
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(50) NOT NULL
            )
        """)
        conn.commit()

# 初期化時にテーブルを作成
create_user_table()

# ルートパスのハンドラ
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # データベースに接続し、データを保存
        with connect_db() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO user_data (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()

    # データベースから保存されたデータを取得
    with connect_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM user_data")
        user_data = cur.fetchall()

    return render_template('index.html', user_data=user_data)

if __name__ == '__main__':
    app.run(debug=True)
