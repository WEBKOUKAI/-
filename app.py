import streamlit as st
import re
import json

# ✅ 必ず最初にセッションキーの初期化
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.title("ログイン")

    with st.form("login_form", clear_on_submit=False):
        password = st.text_input("パスワードを入力してください", type="password", key="login_pw")
        submitted = st.form_submit_button("ログイン（Enterキー対応）")

    if submitted:
        try:
            if st.session_state["login_pw"] == st.secrets["auth"]["password"]:
                st.session_state["authenticated"] = True
                st.experimental_rerun()
            else:
                st.warning("パスワードが違います")
        except KeyError:
            st.error("Secretsにパスワードが設定されていません")

if not st.session_state["authenticated"]:
    login()
    st.stop()


def convert_to_halfwidth(match):
    return match.group(0).translate(str.maketrans(
        "０１２３４５６７８９",
        "0123456789"
    ))

def load_rules(rule_file):
    with open(rule_file, "r", encoding="utf-8") as f:
        return json.load(f)

def apply_rules(text, rules):
    for rule in rules:
        pattern = rule["pattern"]
        if "replacement" in rule:
            repl = rule["replacement"]
            text = re.sub(pattern, repl, text)
        elif "replacement_func" in rule and rule["replacement_func"] == "convert_to_halfwidth":
            text = re.sub(pattern, convert_to_halfwidth, text)
    return text

st.title("NHKスタイル 校正ツール")

uploaded_file = st.file_uploader("テキストファイルをアップロード", type=["txt"])
rule_file = "rules.json"

if uploaded_file:
    raw_text = uploaded_file.read().decode("utf-8")
    rules = load_rules(rule_file)
    corrected_text = apply_rules(raw_text, rules)

    st.subheader("校正後のテキスト")
    st.text_area("結果", corrected_text, height=400)

    st.download_button("校正済みテキストをダウンロード", corrected_text, file_name="corrected.txt")
