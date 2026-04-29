import os

import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="住宅購入ナビAI", page_icon="🏠", layout="wide")
st.title("住宅購入ナビAI（MVP）")
st.caption("住宅購入の進行状況に応じて、次にやることとリスクをAIが整理します。")


def bool_to_text(value: bool) -> str:
    return "済" if value else "未"


def build_prompt(
    contract: bool,
    loan: bool,
    kinko: bool,
    insurance: bool,
    address: bool,
    date: str,
    question: str,
) -> str:
    return f"""あなたは住宅購入の専門ナビゲーターです。

以下の状況をもとに、次にやるべきこととリスクを整理してください。

# 状況

* 売買契約: {bool_to_text(contract)}
* 本審査: {bool_to_text(loan)}
* 金消: {bool_to_text(kinko)}
* 火災保険: {bool_to_text(insurance)}
* 住民票: {bool_to_text(address)}
* 決済日: {date}

# ユーザーの質問

{question}

# 出力形式

1. 次にやること（優先度順）
2. リスク（重要なものから）
3. 補足説明（簡潔に）
"""


left_col, center_col, right_col = st.columns([1, 1.2, 1.2])

with left_col:
    st.subheader("状態入力")
    contract = st.checkbox("売買契約済", value=False)
    loan = st.checkbox("本審査済", value=False)
    kinko = st.checkbox("金消済", value=False)
    insurance = st.checkbox("火災保険済", value=False)
    address = st.checkbox("住民票移動済", value=False)
    settlement_date = st.date_input("決済日")

with center_col:
    st.subheader("ユーザー質問入力")
    question = st.text_area(
        "今の状況で気になることを入力してください",
        placeholder="例：来月決済ですが、今週中に何を優先すべきですか？",
        height=220,
    )
    run_button = st.button("AIに相談する", type="primary")

with right_col:
    st.subheader("出力表示")

    if "response_markdown" not in st.session_state:
        st.session_state.response_markdown = "ここにAIの回答が表示されます。"

    st.markdown(st.session_state.response_markdown)


if run_button:
    if not question.strip():
        st.warning("質問を入力してください。")
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("OPENAI_API_KEY が設定されていません。READMEの手順で設定してください。")
        else:
            try:
                client = OpenAI(api_key=api_key)
                prompt = build_prompt(
                    contract=contract,
                    loan=loan,
                    kinko=kinko,
                    insurance=insurance,
                    address=address,
                    date=str(settlement_date),
                    question=question.strip(),
                )

                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=prompt,
                )

                st.session_state.response_markdown = response.output_text
                st.rerun()
            except Exception as e:
                st.error(f"AI呼び出しに失敗しました。時間をおいて再実行してください。\n\n詳細: {e}")


