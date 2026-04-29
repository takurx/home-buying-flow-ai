import streamlit as st
import pandas as pd
import json
from datetime import datetime

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="住宅購入ナビ MVP",
    page_icon="🏠",
    layout="wide"
)

# =========================
# Session State 初期化
# =========================
if "stage" not in st.session_state:
    st.session_state.stage = "本審査前"

if "uncertain_cost" not in st.session_state:
    st.session_state.uncertain_cost = 500000

if "next_action" not in st.session_state:
    st.session_state.next_action = "オプション見積を確定する"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================
# 初期銀行データ
# =========================
banks = [
    {
        "銀行": "SBI新生",
        "金利(%)": 0.64,
        "状況": "本審査前",
        "備考": "延長前提"
    },
    {
        "銀行": "住信SBIネット",
        "金利(%)": 0.95,
        "状況": "代理店進行中",
        "備考": "間に合わせるとのこと"
    },
    {
        "銀行": "PayPay",
        "金利(%)": 0.95,
        "状況": "本審査中",
        "備考": "融資1週間"
    },
    {
        "銀行": "常陽",
        "金利(%)": 1.325,
        "状況": "本審査中",
        "備考": "感触不明"
    },
]

df = pd.DataFrame(banks)

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.title("🏠 購入ステータス")

    st.markdown("### 📍現在地")
    st.info(st.session_state.stage)

    st.markdown("### 💰未確定費用")
    st.warning(f"± {st.session_state.uncertain_cost:,} 円")

    st.markdown("### 👉 次にやること")
    st.success(st.session_state.next_action)

    st.markdown("### 🕒 最終更新")
    st.caption(datetime.now().strftime("%Y-%m-%d %H:%M"))

# =========================
# Header
# =========================
st.title("住宅購入ナビ MVP")
st.caption("住宅購入の進捗・比較・相談を1画面で整理")

# =========================
# 購入フロー
# =========================
st.subheader("① 購入フロー")

flow = [
    "物件探し",
    "仮審査",
    "買付",
    "契約",
    "本審査",
    "金消契約",
    "決済",
    "引渡し"
]

cols = st.columns(len(flow))

for i, step in enumerate(flow):
    with cols[i]:
        if step == st.session_state.stage:
            st.success(step)
        else:
            st.write(step)

# =========================
# 銀行比較
# =========================
st.subheader("② 銀行比較")
st.dataframe(df, use_container_width=True)

# =========================
# 見積アップロード
# =========================
st.subheader("③ 見積アップロード（仮）")

uploaded_file = st.file_uploader(
    "PDF / 画像アップロード",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:
    st.success(f"{uploaded_file.name} を受け取りました")
    st.info("※ 今は保存のみ。次版でOCR解析予定")

# =========================
# 状態JSON
# =========================
state = {
    "stage": st.session_state.stage,
    "uncertain_cost": st.session_state.uncertain_cost,
    "next_action": st.session_state.next_action,
    "banks": banks
}

# =========================
# Chat欄
# =========================
st.subheader("④ AI相談チャット")

for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)

prompt = st.chat_input("今の状況で次にやることは？")

if prompt:
    st.session_state.chat_history.append(("user", prompt))

    # ---- 仮AI応答（OpenAI API接続前） ----
    reply = f"""
現在地は「{state['stage']}」です。

未確定費用は ±{state['uncertain_cost']:,} 円です。

次にやるべきこと：
👉 {state['next_action']}

（この部分は次にOpenAI API接続可能）
"""

    st.session_state.chat_history.append(("assistant", reply))
    st.rerun()

# =========================
# Debug用JSON
# =========================
with st.expander("状態JSON（開発用）"):
    st.code(json.dumps(state, ensure_ascii=False, indent=2), language="json")

