
import streamlit as st
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Câu lạc bộ",
    page_icon="🏀",
    layout="wide"
)

BASE = Path(__file__).resolve().parents[1]
IMAGE_DIR = BASE / "image"
st.markdown("""
<style>
#MainMenu, footer, header {
    visibility: hidden;
}

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
    color: #ffff;
    font-size: 16px;
}

.section-title {i
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
/* Giờ được chọn: màu cam */
div.stButton > button[kind="primary"] {
    background: #ff861f !important;
    color: #222 !important;
    border: 1px solid #ff861f !important;
}
div.stButton > button[kind="secondary"],
div.stButton > button[kind="primary"] {
    background-color: #ff861f !important;
    color: #111111 !important;
    border: 1px solid #ff861f !important;
    border-radius: 10px;
    font-weight: 700;
    margin-top:15px
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
    color:#111111;
    border: none;
}

div[data-testid="stTextInput"] input {
    background: #ffff;
    color: black;
    border: 1px solid #ffff;
    border-radius: 10px;
}

.answer-box {
    background: #ffff;
    border-left: 4px solid #ffff;
    border-radius: 10px;
    padding: 20px;
    margin-top: 18px;
    color: black;
}

.footer {
    text-align: center;
    color: #999999;
    margin-top: 35px;
    padding: 20px;
    border-top: 1px solid #333;
}

""", unsafe_allow_html=True)
st.markdown("""
<div class="navbar">
    <div class="logo">🏀 BasketZone</div>
    <div class="nav-links">
        <a href="/home" target="_self">Trang chủ</a>
        <a href="/club" target="_self">Câu lạc bộ</a>
        <a href="/booking" target="_self">Đặt sân</a>
        <a href="pages/login.py" target="_self">Đăng nhập</a>
        <a href="/register" target="_self">Đăng ký</a>
</div>
""", unsafe_allow_html=True)


st.title("Thông tin câu lạc bộ")

teams = {
    "Los Angeles Lakers": "lakers_logo.png",
    "Chicago Bulls": "Chicago_Bulls_logo.png",
    "Boston Celtics": "boston_logo.png",
    "Golden State Warriors": "golden_state_w_logo.png",
    "New York Knicks": "nyk_logo.png",
    "Miami Heat": "miami_heat_logo.jpg"
}

tk = st.text_input("Tìm kiếm",
    placeholder="Nhập tên đội bóng..."
)

if tk.strip():
    results = [
        name for name in teams
        if tk.strip().lower() in name.lower()
    ]

    if results:
        for name in results:
            st.divider()

            col1, col2 = st.columns([1, 3])

            with col1:
                logo = IMAGE_DIR / teams[name]

                if logo.is_file():
                    st.image(str(logo), width=130)
                else:
                    st.warning("Không tìm thấy ảnh logo.")

            with col2:
                st.subheader(name)
                st.write("Tìm hiểu và gửi đơn đăng ký tham gia câu lạc bộ.")

                if st.button(
                    "Đăng ký tham gia",
                    key="apply_" + name
                ):
                    st.session_state["selected_team"] = name
    else:
        st.warning("Không tìm thấy câu lạc bộ phù hợp.")



selected = st.session_state.get("selected_team")

if selected:
    st.divider()
    st.title("Đơn đăng ký tham gia")
    st.subheader(selected)

    with st.form("form_" + selected):
        full_name = st.text_input("Họ và tên")
        email = st.text_input("Email")
        age = st.number_input(
            "Tuổi",
            min_value=10,
            max_value=100,
            value=16
        )
        experience = st.selectbox(
            "Kinh nghiệm bóng rổ",
            [
                "Mới bắt đầu",
                "Đã chơi phong trào",
                "Đã tham gia câu lạc bộ",
                "Thi đấu cấp trường/đội tuyển"
            ]
        )
        reason = st.text_area("Lý do muốn tham gia")

        if st.form_submit_button("Gửi đơn đăng ký",type="primary"):
            if not full_name.strip() or not email.strip() or "@" not in email:
                st.error("Vui lòng nhập họ tên và email hợp lệ.")
            else:
                st.success(
                    f"Đã ghi nhận đơn đăng ký của {full_name} "
                    f"vào câu lạc bộ {selected}!"
                )
