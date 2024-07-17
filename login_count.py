import streamlit as st

# クエリパラメータからユーザーIDを取得
query_params = st.experimental_get_query_params()
user_id = query_params.get('user_id', [None])[0]

if user_id is None:
    st.write("ユーザーIDが提供されていません。URLに ?user_id=example を追加してください。")
else:
    # セッションステートを使用してユーザーごとの接続回数を管理
    if 'visit_counts' not in st.session_state:
        st.session_state.visit_counts = {}

    if user_id not in st.session_state.visit_counts:
        st.session_state.visit_counts[user_id] = 0

    st.session_state.visit_counts[user_id] += 1

    st.write(f"ユーザー {user_id} の接続回数: {st.session_state.visit_counts[user_id]}")

    # すべてのユーザーの接続回数を表示（デバッグ用）
    st.write("全ユーザーの接続回数:")
    st.write(st.session_state.visit_counts)
