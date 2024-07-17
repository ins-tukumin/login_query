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

if user_id is None:
    st.write("ユーザーIDが提供されていません。URLに ?user_id=example_user を追加してください。")
else:
    try:
        c.execute('BEGIN TRANSACTION')
        
        c.execute('SELECT count FROM visits WHERE user_id = ?', (user_id,))
        row = c.fetchone()
        if row is None:
            count = 1
            c.execute('INSERT INTO visits (user_id, count) VALUES (?, ?)', (user_id, count))
        else:
            count = row[0] + 1
            c.execute('UPDATE visits SET count = ? WHERE user_id = ?', (count, user_id))
        
        c.execute('COMMIT')
        
        if count == 1:
            st.write(f"ようこそ、ユーザー {user_id} さん。これが初回のアクセスです。")
        else:
            st.write(f"お帰りなさい、ユーザー {user_id} さん。これが {count} 回目のアクセスです。")

        c.execute('SELECT * FROM visits')
        all_visits = c.fetchall()
        st.write("全ユーザーの接続回数:")
        st.write(all_visits)
    except sqlite3.OperationalError as e:
        st.write("データベースにアクセスできませんでした。しばらく待ってから再試行してください。")

if st.button('データベースをクリア'):
    clear_database()
    st.write("データベースをクリアしました。")

conn.close()
