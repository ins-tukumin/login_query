import streamlit as st

# クエリパラメータを取得
query_params = st.experimental_get_query_params()

# クエリパラメータからlogin_idを取得
login_id = query_params.get('login_id', [None])[0]

# 取得したlogin_idを表示
if login_id:
    st.write(f"受け取ったログインID: {login_id}")
else:
    st.write("ログインIDが見つかりませんでした。")

# 必要に応じて、login_idに基づいて処理を行う
# 例: データベースからユーザー情報を取得するなど
if login_id:
    # ここで任意の処理を行う
    st.write(f"ログインID {login_id} に基づいて処理を行います。")
