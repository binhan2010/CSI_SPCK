import streamlit as st
import json
import re
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
#MainMenu,
footer,
header {
    visibility: hidden;
}

[data-testid="stSidebar"] {
    display: none;
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

.logo {
    color: #ff861f;
    font-size: 25px;
    font-weight: 800;
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
def validate_username(username):
    if not username:
        return "Vui lòng nhập username."

    if len(username) < 3:
        return "Username phải có ít nhất 3 ký tự."

    if len(username) > 20:
        return "Username không được vượt quá 20 ký tự."

    if not re.fullmatch(r"[a-zA-Z0-9_]+", username):
        return "Username chỉ được chứa chữ cái, chữ số và dấu _."

    return None
def validate_password(password):
    if not password:
        return "Vui lòng nhập mật khẩu."

    if len(password) < 8:
        return "Mật khẩu phải có ít nhất 8 ký tự."

    if len(password) > 128:
        return "Mật khẩu không được vượt quá 128 ký tự."

    if not re.search(r"[A-Z]", password):
        return "Mật khẩu phải có ít nhất 1 chữ hoa."

    if not re.search(r"[a-z]", password):
        return "Mật khẩu phải có ít nhất 1 chữ thường."

    if not re.search(r"\d", password):
        return "Mật khẩu phải có ít nhất 1 chữ số."

    if not re.search(r"[^A-Za-z0-9]", password):
        return "Mật khẩu phải có ít nhất 1 ký tự đặc biệt."

    return None
with st.container(border=True):
    st.subheader("Đăng nhập")
    username = st.text_input(
        "Username",
        placeholder="Nhập tên đăng nhập"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Nhập mật khẩu"
    )
    if st.button("Đăng nhập", use_container_width=True):

        username = username.strip()
        username_error = validate_username(username)
        password_error = validate_password(password)
        if username_error:
            st.error(username_error)
        if password_error:
            st.error(password_error)
        if not username_error and not password_error:
            if not file_path.exists():
                st.error("Chưa tìm thấy file users.json.")
            else:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        users = json.load(file)
                    if not isinstance(users, dict):
                        st.error("Dữ liệu users.json không hợp lệ.")

                    else:
                        found = False
                        for user in users.values():
                            if not isinstance(user, dict):
                                continue
                            if (
                                user.get("username") == username
                                and user.get("password") == password
                            ):
                                found = True
                                break
                        if found:

                            st.session_state["logged_in"] = True
                            st.session_state["username"] = username
                            st.switch_page(str(BASE_DIR / "home.py"))
                        else:
                            st.error(
                                "Username hoặc mật khẩu không chính xác."
                            )
                except (json.JSONDecodeError, OSError):
                    st.error(
                        "Không thể đọc dữ liệu tài khoản. "
                        "Hãy kiểm tra file users.json."
                    )
