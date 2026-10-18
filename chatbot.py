import streamlit as st
import google.genai as genai
from google.genai import types
from config import GEMINI_API_KEY


st.set_page_config(page_title="Chatbot",layout = "wide",initial_sidebar_state="collapsed")
st.title("Basket Chatbot")
with st.sidebar:
    st.markdown("**Một vào câu hỏi gợi ý:**")
    st.markdown("- Hôm nay có những đội nào thi đấu với nhau?")
    st.markdown("- Đội Knicks nay có thi đấu không?")
    st.markdown("- Thành viện của đội Boston gồm những ai?")

prompt = st.text_input(
    "Đặt câu hỏi",
    placeholder="Nhập câu hỏi của bạn tại đây..."
)

client = genai.Client(api_key=GEMINI_API_KEY)

if st.button("Gửi"):
    if prompt.strip():
        with st.spinner("..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=(
                            "Bạn là một chuyên gia về bóng rổ và hiểu biết về các trận thi đấu bóng rổ trên toàn cầu"
                            "Hãy trả lời bằng tiếng việt "
                            "Trả lời ngắn gọn,đầy đủ"
                        )
                    )
                )

                st.markdown(response.text)

            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {e}")
    else:
        st.warning("Nhập lại ccaua hỏi")


