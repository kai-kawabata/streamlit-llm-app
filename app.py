from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from openai import OpenAI
import os

def get_llm_answer(input_message: str, expert_type: str) -> str:
    """
    入力テキストと専門家選択値を受け取り、LLM回答を返す関数
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        return "OPENAI_API_KEYが設定されていません。envファイルを確認してください。"

    if expert_type == "健康アドバイザー":
        system_message = "あなたは健康に関するアドバイザーです。安全なアドバイスを提供してください。"
    elif expert_type == "旅行アドバイザー":
        system_message = "あなたは旅行に関するアドバイザーです。安全で楽しい旅行プランやアドバイスを提供してください。"
    else:
        system_message = "あなたはユーザーの質問に対して適切なアドバイスを提供してください。"

    client = OpenAI(api_key=openai_api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": input_message}
        ],
        temperature=0.5
    )
    return completion.choices[0].message.content


st.title("LLM 質問アプリ")
st.markdown("""
このWebアプリは、OpenAIのLLM（大規模言語モデル）を活用し、選択した専門家（健康アドバイザーまたは旅行アドバイザー）として質問に回答します。

【操作方法】
1. 画面上部のラジオボタンで、相談したい専門家の種類を選択してください。
2. 質問内容を入力フォームに記入してください。
3. 「送信」ボタンを押すと、選択した専門家としてLLMが回答を返します。

""")

# 専門家の種類を選択
expert_type = st.radio(
    "専門家の種類を選択してください",
    ("健康アドバイザー", "旅行アドバイザー")
)

input_message = st.text_input(label="質問してください。")

if st.button("送信") and input_message:
    with st.spinner("回答生成中..."):
        answer = get_llm_answer(input_message, expert_type)
    st.write("### 回答")
    st.write(answer)