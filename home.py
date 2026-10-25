import streamlit as st
import google.genai as genai
from google.genai import types
from config import GEMINI_API_KEY, NBA_API_KEY
st.set_page_config(
    page_title="Trang chủ",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu, footer, header {
    visibility: hidden;
}
/*ẨNn side bar*/
[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.stApp {
    # background: linear-gradient(135deg, #101010, #202020);
    background:#ffff
    color:white;
}

.navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 75px;
    box-sizing: border-box;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 15, 15, 0.96);
    border-bottom: 1px solid #333;
    padding: 0 40px;
    z-index: 9999;
    margin-top:0;
    border-radius: 0;
}


.logo {
    color: #ff861f;
    font-size: 25px;
    font-weight: 800;
}

.nav-links {
    display: flex;
    gap: 22px;
    flex-wrap: wrap;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-weight: 600;
    font-size: 14px;
}

.nav-links a:hover {
    color: #ff861f;
}

.hero {
    background: linear-gradient(110deg, #252525, #171717);
    border: 1px solid #393939;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
    margin-top:40px;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 12px;
    color: white;
}

.orange {
    color: #ff861f;
}

.hero p {
    color: #cccccc;
    font-size: 16px;
}

.section-title {
    font-size: 23px;
    font-weight: 750;
    margin: 20px 0 12px;
}

.question-card {
    background: #222222;
    border: 1px solid #393939;
    border-radius: 12px;
    padding: 14px;
    min-height: 95px;
    color: #eeeeee;
}

div.stButton > button {
    background: #ff861f;
    color: #111111;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    min-height: 43px;
}

div.stButton > button:hover {
    background: #ff9b43;
    color: #111111;
    border: none;
}

div[data-testid="stTextInput"] input {
    background: #252525;
    color: white;
    border: 1px solid #555;
    border-radius: 10px;
}

.answer-box {
    background: #222222;
    border-left: 4px solid #ff861f;
    border-radius: 10px;
    padding: 20px;
    margin-top: 18px;
    color: white;
}




.footer {
    text-align: center;
    color: #999999;
    margin-top: 35px;
    padding: 20px;
    border-top: 1px solid #333;
}

.st-key-chat_toggle {
    position: fixed;
    right: 25px;
    bottom: 22px;
    z-index: 10000;
}

.st-key-chat_toggle button {
    width: 62px;
    height: 62px;
    border-radius: 50px;
    background: #ff861f;
    color: #111111;
    border: none;
    font-size: 27px;
    box-shadow: 0 4px 15px #0004;
}

.st-key-chat_toggle button:hover {
    background: #ff9b43;
    color: #111111;
    border: none;
}


.st-key-chat_panel {
    position: fixed;
    right: 25px;
    bottom: 100px;
    width: 360px;
    max-width: calc(100vw - 35px);
    height: 480px;
    overflow-y: auto;
    z-index: 9999;
    background: #ffff;
    border: 1px solid #ff861f;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 30px #0005;
}

/* input*/
.st-key-chat_panel input {
    background: white;
    color: black;
}

.st-key-chat_panel [data-testid="stChatMessage"] {
    background: #ffff;
    border-radius: 10px;
    padding: 8px;

}


</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="navbar">
    <div class="logo">BasketZone</div>
    <div class="nav-links">
        <a href="home.py" target="_self">Trang chủ</a>
        <a href="/club" target="_self">Câu lạc bộ</a>
        <a href="/booking" target="_self">Đặt sân</a>
        <a href="/login" target="_self">Đăng nhập</a>
        <a href="/register" target="_self">Đăng ký</a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chatbot-tooltip">
</div>

<a href="/chatbot" target="_self" class="chatbot-float"
   title="Chat với Basket AI">
</a>
""", unsafe_allow_html=True)


left, right = st.columns([1.3, 1])

with left:
    st.markdown("""
    <div class="hero">
        <h1>Basketball <span class="orange">AI Assistant</span></h1>
        <p>
            Trợ lý bóng rổ của BasketZone.
            Hỏi về các đội bóng, cầu thủ, luật chơi
            và kiến thức bóng rổ.
        </p>
        <p>Hỏi đáp thông minh &nbsp; | &nbsp;
           Phản hồi nhanh</p>
    </div>
    """, unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)

if "prompt" not in st.session_state:
    st.session_state.prompt = ""

with col1:
    st.markdown("""
    <div class="question-card">
        <b>Lịch thi đấu</b><br><br>
        Tìm hiểu các trận đấu bóng rổ.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Hỏi về lịch thi đấu", use_container_width=True):
        st.session_state.prompt = (
            "Hãy cho tôi biết cách xem lịch thi đấu NBA mới nhất."
        )

with col2:
    st.markdown("""
    <div class="question-card">
        <b>Câu lạc bộ</b><br><br>
        Khám phá các đội bóng nổi tiếng.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Hỏi về đội Knicks", use_container_width=True):
        st.session_state.prompt = (
            "Giới thiệu về đội bóng New York Knicks."
        )

with col3:
    st.markdown("""
    <div class="question-card">
        <b>Cầu thủ</b><br><br>
        Tìm hiểu cầu thủ và thành tích.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Hỏi về cầu thủ", use_container_width=True):
        st.session_state.prompt = (
            "Giới thiệu một số cầu thủ NBA nổi tiếng."
        )
if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

if "mini_messages" not in st.session_state:
    st.session_state.mini_messages = [
        {
            "role": "assistant",
            "content": "Xin chào!Mình có thể giúp gì về bóng rổ?"
        }
    ]

# đóng và mở
if st.button("", key="chat_toggle"):
    st.session_state.chat_open = not st.session_state.chat_open

# appear
if st.session_state.chat_open:
    with st.container(key="chat_panel"):

        title_col, close_col = st.columns([5, 1])

        with title_col:
            st.markdown(
                "<h3 style='color:#ff861f;margin:0;'>Basket AI</h3>",
                unsafe_allow_html=True
            )

        with close_col:
            if st.button("✖", key="close_chat"):
                st.session_state.chat_open = False
                st.rerun()

        st.caption("Trợ lý bóng rổ BasketZone")
        st.divider()

        for message in st.session_state.mini_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question_chat = st.chat_input(
            "Nhập câu hỏi về bóng rổ...",
            key="mini_chat_input"
        )

        if question_chat:
            # ques ng dùng
            st.session_state.mini_messages.append({
                "role": "user",
                "content": question_chat
            })
            #model AI
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)

                with st.spinner("Basket AI đang trả lời..."):
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=[
                            {
                                "role": (
                                    "user" if m["role"] == "assistant"
                                    else m["role"]
                                ),
                                "parts": [{"text": m["content"]}]
                            }
                            for m in st.session_state.mini_messages
                            if m["role"] == "user"
                        ],
                        config=types.GenerateContentConfig(
                            system_instruction=(
                                "Bạn là Basket AI, trợ lý bóng rổ. "
                                "Trả lời bằng tiếng Việt, ngắn gọn, "
                                "dễ hiểu. Không bịa dữ liệu lịch thi đấu."
                            )
                        )
                    )

                answer = response.text or "Bạn hãy thử hỏi lại nhé!"

            except Exception as e:
                answer = f"Đã xảy ra lỗi: {e}"

            st.session_state.mini_messages.append({
                "role": "assistant",
                "content": answer
            })

            st.rerun()

st.markdown("""
<div class="footer">
    <b>BasketZone</b><br>
    Kết nối đam mê bóng rổ của bạn.
</div>
""", unsafe_allow_html=True)
