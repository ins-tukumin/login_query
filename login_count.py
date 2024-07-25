import streamlit as st
import sqlite3

# データベース接続の初期化
conn = sqlite3.connect('visits.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS visits (user_id TEXT PRIMARY KEY, count INTEGER)''')
conn.commit()

# グループごとのURLを定義
group_urls = {
    "group1": "hhttps://ragepre.streamlit.app/",
    "group2": "https://llmrel.streamlit.app/",
    "group3": "https://www.google.com/maps"
}

# participants.txtファイルからIDとグループを読み込む関数
def load_participants(file_path):
    participants = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    user_id, group = line.split(',')
                    participants[user_id] = group
    except FileNotFoundError:
        st.error("参加者リストファイルが見つかりません。")
    return participants

# クエリパラメータからユーザーIDを取得
query_params = st.experimental_get_query_params()
user_id = query_params.get('login_id', [None])[0]

# データベースのクリア
def clear_database():
    c.execute('DELETE FROM visits')
    conn.commit()

# 参加者のリストを読み込む
participants = load_participants('participants2.txt')

if user_id is None:
    # クエリパラメータがない場合は、ユーザーにIDを入力させる
    user_id = st.text_input("ユーザーIDを入力してください:")

if user_id:
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
            # ユーザーIDからグループを決定
            group = participants.get(user_id)
            if group:
                group_url = group_urls.get(group)
                if group_url:
                    group_url_with_id = f"{group_url}?user_id={user_id}"
                    # Metaタグを使ってリダイレクト
                    st.markdown(f'''
                        <meta http-equiv="refresh" content="0; url={group_url_with_id}">
                    ''', unsafe_allow_html=True)
                else:
                    st.write("対応するグループURLが見つかりません。")
            else:
                st.write("ユーザーIDに対応するグループが見つかりません。")
        else:
            st.write("これにて実験は終了です。タブを閉じて構いません。ご協力ありがとうございました。")

        c.execute('SELECT * FROM visits')
        all_visits = c.fetchall()
        st.write("全ユーザーの接続回数:")
        st.write(all_visits)
    except sqlite3.OperationalError as e:
        st.write("データベースにアクセスできませんでした。しばらく待ってから再試行してください。")
    except Exception as e:
        st.write(f"エラーが発生しました: {e}")
else:
    st.write("ユーザーIDが提供されていません。URLに ?user_id=example_user を追加するか、上記のテキストボックスに入力してください。")

if st.button('データベースをクリア'):
    clear_database()
    st.write("データベースをクリアしました。")
    st.experimental_rerun()

conn.close()

# アプリケーションを実行するには、以下のコマンドを使用します
# streamlit run app.py
