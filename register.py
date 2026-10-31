import streamlit as st
import json
import re
import hashlib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

st.set_page_config(
    page_title="Đăng nhập",
    page_icon="🏀",
    initial_sidebar_state="collapsed"
)

file_path = Path(__file__).parent / "users.json"
BASE_DIR = Path(__file__).resolve().parents[1]

st.markdown("""
<style>
#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    display: none;
}

.logo {
    color: #ff861f;
    font-size: 25px;
    font-weight: 800;
}
.block-container {
    padding-top: 5rem;
    padding-bottom: 2rem;
    max-width: 450px;
}

.stApp {
    background: #ffffff;
    color: #222222;
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
    background: #ffffff;
    color: black;
    border: 1px solid #dddddd;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <div class="logo">🏀 BasketZone</div>
    <div class="nav-links">
        <a href="/home" target="_self">Trang chủ</a>
        <a href="/club" target="_self">Câu lạc bộ</a>
        <a href="/booking" target="_self">Đặt sân</a>
        <a href="/login" target="_self">Đăng nhập</a>
        <a href="/register" target="_self">Đăng ký</a>
    </div>
</div>
""", unsafe_allow_html=True)

def load_users():
    if not file_path.exists():
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def validate_username(name):
    if len(name) < 3 or len(name) > 20 or not re.fullmatch(r"[a-zA-Z0-9_]+", name):
        return "Username phải từ 3-20 ký tự, gồm chữ cái, số hoặc _."
    return None

def validate_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(pattern, email):
        return "Email không đúng định dạng."
    if len(email) > 254:
        return "Email quá dài."
    return None

def validate_password(pw):
    if len(pw) < 8:
        return "Mật khẩu phải từ 8 ký tự trở lên."
    if not re.search(r"[A-Z]", pw):
        return "Mật khẩu phải có ít nhất 1 chữ hoa."
    if not re.search(r"[a-z]", pw):
        return "Mật khẩu phải có ít nhất 1 chữ thường."
    if not re.search(r"\d", pw):
        return "Mật khẩu phải có ít nhất 1 số."
    if not re.search(r"[^A-Za-z0-9]", pw):
        return "Mật khẩu phải có ít nhất 1 ký tự đặc biệt."
    return None

st.title("Đăng ký tài khoản")

username = st.text_input("Username", placeholder="Nhập tên đăng ký")
email = st.text_input("Email", placeholder="Nhập email").lower()
password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu")
confirm_pw = st.text_input("Xác nhận mật khẩu", type="password", placeholder="Nhập lại mật khẩu")

if st.button("Đăng ký"):
    users = load_users()
    err = validate_username(username) or validate_email(email) or validate_password(password)
    if err:
        st.error(err)
    elif password != confirm_pw:
        st.error("Mật khẩu xác nhận không khớp.")
    elif email in users:
        st.error("Email này đã được đăng ký.")
    else:
        users[email] = {"username": username, "email": email, "password": password}
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
            st.success("Đăng ký thành công!")
        except:
            st.error("Lỗi lưu dữ liệu, vui lòng thử lại.")
