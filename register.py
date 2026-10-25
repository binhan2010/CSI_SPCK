import streamlit as st
import base64
import json
import re
import hashlib
import secrets
from pathlib import Path

st.set_page_config(page_title="Đăng ký", page_icon="🏀")
file_path = Path(__file__).parent / "users.json"

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
    width:450px;
    margin-top:50px;
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


.orange {
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
    background:#ffff;
    color: black;
    border: 1px solid #ffff;
    border-radius: 10px;
}

.answer-box {
    background: #ffff;
    border-left: 4px solid #ff861f;
    border-radius: 10px;
    padding: 20px;
    margin-top: 18px;
    color: #ffff;
}

.footer {
    text-align: center;
    color: #999999;
    margin-top: 35px;
    padding: 20px;
    border-top: 1px solid #333;
}

/* Nút chat nổi */
.st-key-chat_toggle {
    position: fixed;
    right: 25px;
    bottom: 22px;
    z-index: 10000;
}

.st-key-chat_toggle button {
    width: 62px;
    height: 62px;
    border-radius: 50%;
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

/* Khung chat mini */
.st-key-chat_panel {
    position: fixed;
    right: 25px;
    bottom: 100px;
    width: 360px;
    max-width: calc(100vw - 35px);
    height: 480px;
    overflow-y: auto;
    z-index: 9999;
    background: #181818;
    border: 1px solid #ff861f;
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 8px 30px #0005;
}

/* Ô nhập trong khung chat */
.st-key-chat_panel input {
    background: #292929;
    color: white;
}

.st-key-chat_panel [data-testid="stChatMessage"] {
    background: #252525;
    border-radius: 10px;
    padding: 8px;
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
""", unsafe_allow_html=True)
def load_users():
    if not file_path.exists():
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            users = json.load(f)

        if isinstance(users, dict):
            return users

        return {}

    except (json.JSONDecodeError, OSError):
        return {}


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        600000
    ).hex()

    return {
        "salt": salt,
        "password_hash": hashed
    }

def validate_username(username):
    username = username.strip()

    if not username:
        return "Vui lòng nhập username."

    if len(username) < 3:
        return "Username phải có ít nhất 3 ký tự."

    if len(username) > 20:
        return "Username không được vượt quá 20 ký tự."

    if not re.fullmatch(r"[a-zA-Z0-9_]+", username):
        return (
            "Username chỉ được chứa chữ cái, "
            "chữ số và dấu gạch dưới (_)."
        )

    return None
def validate_email(email):
    email = email.strip()

    if not email:
        return "Vui lòng nhập email."

    pattern = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"

    if not re.fullmatch(pattern, email):
        return "Email không đúng định dạng. Ví dụ: abc@gmail.com"

    if len(email) > 254:
        return "Email quá dài."

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

    st.subheader("Đăng ký")

    username = st.text_input(
        "Username",
        placeholder="Nhập tên đăng ký",
        key="username"
    )
    email = st.text_input(
        "Email",
        placeholder="Nhập email",
        key="email"
    )
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Nhập mật khẩu",
        key="password"
    )
    confirm_password = st.text_input(
        "Xác nhận mật khẩu",
        type="password",
        placeholder="Nhập lại mật khẩu",
        key="confirm_password"
    )
    register = st.button(
        "Đăng ký",
        use_container_width=True
    )
    if register:
        username = username.strip()
        email = email.strip().lower()
        users = load_users()
        username_error = validate_username(username)
        email_error = validate_email(email)
        password_error = validate_password(password)
        if username_error:
            st.error(username_error)
        if email_error:
            st.error(email_error)
        if password_error:
            st.error(password_error)
        if password != confirm_password:
            st.error("Mật khẩu xác nhận không khớp.")
        if not email_error and email in users:
            st.error("Email này đã được đăng ký.")
        if (
            not username_error
            and not email_error
            and not password_error
            and password == confirm_password
            and email not in users
        ):
            password_data = hash_password(password)
            users[email] = {
                "username": username,
                "email": email,
                "salt": password_data["salt"],
                "password_hash": password_data["password_hash"]
            }
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(
                        users,
                        f,
                        ensure_ascii=False,
                        indent=4
                    )
                st.success(" Đăng ký thành công!")
            except OSError:
                st.error("Không thể lưu được tài khoản. Vui lòng thử lại.")
    st.markdown("<br>", unsafe_allow_html=True)
