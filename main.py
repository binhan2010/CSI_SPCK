import streamlit as st

bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #D6E4F0;
}
</style>
"""
st.markdown(bg_css, unsafe_allow_html=True)

st.set_page_config(
    page_title="Basketball Assistant",
    page_icon="🏀🏀🏀",
)

APP_NAME = "bot"
APP_TAGLINE = "Trợ lý ảo giúp bạn theo dõi lịch thi đấu bóng rổ và trả lời câu hỏi về bóng rổ !!!!!"
SUGGESTED_QUESTIONS = [
    "Hôm nay có trận nào diễn ra không?",
    "Đội Lakers thi đấu khi nào?",
    "Cho tôi lịch thi đấu tuần này",
]


with st.sidebar:
    bg_sidebar_css = """<style>[data-testid="stAppViewContainer"]  {background-color:#FFE4E1}"""
    st.markdown(bg_sidebar_css,unsafe_allow_html= True)
    
    st.markdown("**Gợi ý câu hỏi:**")
    clicked_question = None
    for q in SUGGESTED_QUESTIONS:
        if st.button(q, key=f"suggest_{q}", use_container_width=True):
            clicked_question = q




col_icon, col_title = st.columns([1, 10])
with col_icon:
    st.markdown("<h1 style='font-size:48px;'>🏀</h1>", unsafe_allow_html=True)
with col_title:
    st.markdown("<h1 style='font-size:48px;'>Basketball Assistant</h1>",unsafe_allow_html=True)

st.write(APP_TAGLINE)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Chào bạn, tôi là {APP_NAME}. Tôi có thể giúp bạn tra cứu lịch thi đấu, "
                       f"tỷ số và thông tin các đội bóng rổ.",
        }
    ]

for msg in st.session_state.messages:
    avatar = "🏀" if msg["role"] == "assistant" else None
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])


