import streamlit as st
import google.genai as genai
import requests
import time,random
from zoneinfo import ZoneInfo
from datetime import datetime
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
    background: #ffff;
    color: #111111;
    border: none;
}

div[data-testid="stTextInput"] input {
    background: #ffff;
    color: black;
    border: 1px;
    border-radius: 10px;
}

.answer-box {
    background: #222222;
    border-left: 4px solid;
    border-radius: 10px;
    padding: 20px;
    margin-top: 18px;
    color: white;
}




/* NÚT CHAT GÓC PHẢI */
.st-key-chat_toggle {
    position: fixed;
    right: 25px;
    bottom: 22px;
    z-index: 10000;
}

.st-key-chat_toggle button {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    background: #ffff;
    color: black;
    border: none;
    font-size: 24px;
    box-shadow: 0 4px 15px #0004;
}

.st-key-chat_toggle button:hover {
    background: #ffff;
    color: black;
    border: none;
}



.footer {
    text-align: center;
    color: #999999;
    margin-top: 35px;
    padding: 20px;
    border-top: 1px solid #333;
}</style>""",unsafe_allow_html=True)


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
        <p>Hỏi đáp thông minh &nbsp</p>
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

client = genai.Client(api_key=GEMINI_API_KEY)
st.markdown("""
<style>

/* Nút chat góc phải */
.st-key-chat_toggle {
    position: fixed;
    right: 25px;
    bottom: 22px;
    z-index: 10000;
}

.st-key-chat_toggle button {
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: #ff861f;
    color: #111;
    border: none;
    font-size: 24px;
    box-shadow: 0 4px 15px #0005;
}

.st-key-chat_toggle button:hover {
    background: #ff9b43;
    color: #111;
    border: none;
}

/* Khung chat */
.st-key-chat_panel {
    position: fixed;
    right: 25px;
    bottom: 95px;
    width: 360px;
    max-width: calc(100vw - 35px);
    height: 480px;
    overflow-y: auto;
    z-index: 9999;
    background: #ffff;
    border: 1px solid #ffff;
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 8px 30px #0005;
}

/* Tin nhắn */
.st-key-chat_panel [data-testid="stChatMessage"] {
    background: #ffff;
    border-radius: 10px;
    padding: 8px;
}

/* Ô nhập */
.st-key-chat_panel input {
    background: #ffff;
    color:black;
    border: 1px ;
    border-radius: 8px;
}

/* Nút gửi */
.st-key-chat_panel button {
    background: #ff861f;
    color: #111;
    border: none;
}

</style>
""", unsafe_allow_html=True)
#chatbot
@st.cache_data(ttl=300, show_spinner=False)
def get_nba_schedule():
    try:
        today = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).strftime("%Y%m%d")
        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

        response = requests.get(url, params={"dates": today}, timeout=15)
        response.raise_for_status()

        games = []
        for event in response.json().get("events", []):
            competition = event["competitions"][0]
            teams = competition["competitors"]

            home = next((t for t in teams if t["homeAway"] == "home"), None)
            away = next((t for t in teams if t["homeAway"] == "away"), None)

            if not home or not away:
                continue

            game_time = datetime.fromisoformat(
                event["date"].replace("Z", "+00:00")
            ).astimezone(ZoneInfo("Asia/Ho_Chi_Minh"))

            games.append({
                "home": home["team"]["displayName"],
                "away": away["team"]["displayName"],
                "time": game_time.strftime("%H:%M %d/%m/%Y"),
                "status": event["status"]["type"]["detail"],
                "home_score": home.get("score", ""),
                "away_score": away.get("score", "")
            })

        return games, None

    except requests.exceptions.Timeout:
        return None, "ESPN phản hồi quá lâu."
    except requests.exceptions.RequestException as e:
        return None, f"Lỗi kết nối ESPN: {e}"
    except (KeyError, IndexError, ValueError, TypeError) as e:
        return None, f"Lỗi đọc dữ liệu ESPN: {e}"


# nhận biết
def is_schedule_question(question):
    keywords = ["lịch thi đấu", "hôm nay", "trận đấu", "thi đấu khi nào",
                "trận tiếp theo", "sắp tới", "nba games", "schedule"]
    return any(word in question.lower() for word in keywords)


def ask_gemini(question):
    if is_schedule_question(question):
        games, error = get_nba_schedule()

        if error:
            return f"Không thể lấy lịch NBA. {error}"

        if not games:
            return "Hôm nay không có trận NBA nào được ghi nhận trên ESPN."

        schedule = "\n".join(
            f"{g['away']} vs {g['home']} | {g['time']} | {g['status']} | "
            f"Tỉ số: {g['away_score']}-{g['home_score']}"
            for g in games
        )

        instructions = f"""
        Bạn là Basket AI của BasketZone.
        Câu hỏi: {question}
        Dữ liệu NBA từ ESPN:
        {schedule}

        Yêu cầu:
        Trả lời bằng tiếng Việt, rõ ràng.
        Chỉ sử dụng dữ liệu ESPN.
        """
    else:
        instructions = f"""
        Bạn là Basket AI, trợ lý bóng rổ của BasketZone.
        Câu hỏi: {question}
        Hãy trả lời bằng tiếng Việt,ngắn gọn và dễ hiểu.
        """

    for i in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash", contents=instructions
            )
            return response.text or "Bạn hãy thử hỏi lại nhé!"

        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                if i < 2:
                    time.sleep(2 ** i)
                    continue
                return "Gemini đang quá tải. Bạn thử lại sau nhé!"

            return f"Gemini đang gặp lỗi: {e}"

    return "Không thể nhận câu trả lời từ Gemini."

if "mini_open" not in st.session_state:
    st.session_state.mini_open = False

if "mini_messages" not in st.session_state:

    st.session_state.mini_messages = [
        {
            "role": "assistant",
            "content": "Basket AI xin chào bạn"
        }
    ]
if st.button("", key="chat_toggle"):
    st.session_state.mini_open = not st.session_state.mini_open
    st.rerun()

if st.session_state.mini_open:
    with st.container(key="chat_panel"):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.markdown("<h3 style='color:#ff861f;margin:0;'>Basket AI</h3>", unsafe_allow_html=True)

        with col2:
            if st.button("✖", key="close_chat"):
                st.session_state.mini_open = False
                st.rerun()

        st.caption("Trợ lý bóng rổ BasketZone")
        st.divider()

        for msg in st.session_state.mini_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        with st.form("mini_chat_form", clear_on_submit=True):
            question = st.text_input("Câu hỏi", placeholder="Nhập câu hỏi về bóng rổ...", label_visibility="collapsed")
            send = st.form_submit_button("Gửi", use_container_width=True)

        if send and question.strip():
            st.session_state.mini_messages.append({"role": "user", "content": question})

            with st.spinner("Basket AI đang trả lời..."):
                answer = ask_gemini(question)

            st.session_state.mini_messages.append({"role": "assistant", "content": answer})
            st.rerun()


st.markdown("""
<div class="footer">
    <b>BasketZone</b><br>
    Kết nối đam mê bóng rổ của bạn.
</div>
""", unsafe_allow_html=True)
