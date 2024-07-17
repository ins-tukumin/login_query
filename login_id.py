import streamlit as st

# ユーザーからログインIDを取得
login_id = st.text_input("ログインIDを入力してください")

# ボタンを押したときにQualtricsのアンケートURLにリダイレクト
if st.button("アンケートに進む"):
    # QualtricsのアンケートURL
    qualtrics_url = "https://nagoyapsychology.qualtrics.com/jfe/form/SV_1H4rEHXCmTh8RxA"
    # クエリパラメータとしてログインIDを追加
    full_url = f"{qualtrics_url}?login_id={login_id}"
    # リダイレクト
    st.write(f"[こちらをクリックしてアンケートに進む]({full_url})")
