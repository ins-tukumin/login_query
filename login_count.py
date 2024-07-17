import streamlit as st
import sqlite3

# データベース接続の初期化
conn = sqlite3.connect('visits.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS visits (user_id TEXT PRIMARY KEY, count INTEGER)''')
conn.commit()

# クエリパラメータからユーザーIDを取得
query_params = st.experimental_get_query_params()
user_id = query_params.get('login_id', [None])[0]

# データベースのクリア
def clear_database():
    c.execute('DELETE FROM visits')
    conn.commit()

# ユーザーIDが提供されていない場合のエラーメッセージ
if user_id is None:
    st.write("ユーザーIDが提供されていません。URLに ?user_id=example_user を追加してください。")
else:
    # カウンターを読み込むまたは初期化
    c.execute('SELECT count FROM visits WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    if row is None:
        count = 1
        c.execute('INSERT INTO visits (user_id, count) VALUES (?, ?)', (user_id, count))
    else:
        count = row[0] + 1
        c.execute('UPDATE visits SET count = ? WHERE user_id = ?', (count, user_id))
    conn.commit()

    # 現在のユーザーの接続回数を表示
    st.write(f"ユーザー {user_id} の接続回数: {count}")

    # デバッグ用: すべてのユーザーの接続回数を表示
    c.execute('SELECT * FROM visits')
    all_visits = c.fetchall()
    st.write("全ユーザーの接続回数:")
    st.write(all_visits)

# データベースをクリアするボタン
if st.button('データベースをクリア'):
    clear_database()
    st.write("データベースをクリアしました。")

# データベース接続を閉じる
conn.close()
