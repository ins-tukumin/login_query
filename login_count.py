import streamlit as st

# クエリパラメータからユーザーIDを取得
query_params = st.experimental_get_query_params()
user_id = query_params.get('user_id', [None])[0]

# ユーザーIDが提供されていない場合のエラーメッセージ
if user_id is None:
    st.write("ユーザーIDが提供されていません。URLに ?user_id=example_user を追加してください。")
else:
    # セッションステートを使用してユーザーごとの接続回数を管理
    if 'visit_counts' not in st.session_state:
        st.session_state.visit_counts = {}

    # セッションステートにユーザーのカウントが存在しない場合の初期化
    if user_id not in st.session_state.visit_counts:
        st.session_state.visit_counts[user_id] = 0

    # ユーザーの接続回数を増加
    st.session_state.visit_counts[user_id] += 1

    # 現在のユーザーの接続回数を表示
    st.write(f"ユーザー {user_id} の接続回数: {st.session_state.visit_counts[user_id]}")

    # デバッグ用: すべてのユーザーの接続回数を表示
    st.write("全ユーザーの接続回数:")
    st.write(st.session_state.visit_counts)
