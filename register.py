import streamlit as st
import base64
import json
import re
import hashlib
import secrets
from pathlib import Path

st.set_page_config(page_title="Đăng ký", page_icon="🏀")

# image_path = Path(r"E:\CSI\spck_csi\image\bg1.png")
file_path = Path(__file__).parent / "users.json"
BASE_DIR = Path(__file__).resolve().parents[1]
BG_PATH = BASE_DIR / "image" / "bg.jpg"

st.set_page_config(page_title="Login", page_icon="🏀",initial_sidebar_state="collapsed")

# with open(image_path, "rb") as file:
#     image = base64.b64encode(file.read()).decode()

# st.markdown(
#     f"""
#     <style>
#     .stApp {{
#         background: transparent !important;
#     }}

#     .stApp::before {{
#         content: "";
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background-image: url("data:image/png;base64,{image}");
#         background-size: cover;
#         background-position: center;
#         background-repeat: no-repeat;
#         z-index: -2;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown("""
#     <style>
#         [data-testid="stSidebar"] {
#             display: none;
#         }

#         [data-testid="stSidebarCollapsedControl"] {
#             display: none;
#         }
#     </style>
# """, unsafe_allow_html=True)
if BG_PATH.exists():
    with open(BG_PATH, "rb") as file:
        image = base64.b64encode(file.read()).decode()
else:
    image = ""
    st.error(f"Không tìm thấy file ảnh nền tại: {BG_PATH}")
st.markdown(
    f"""
    <style>
        .stApp {{
            background: transparent !important;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image:
                linear-gradient(rgba(10, 20, 40, 0.8),
                                rgba(10, 20, 40, 0.8)),
                url("data:image/jpeg;base64,{image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed; 
            z-index: -2;
        }}
        [data-testid="stSidebar"] {{
            display: none;
        }}
        [data-testid="stSidebarCollapsedControl"] {{
            display: none;
        }}
        h3, 
        [data-testid="stSubheader"] h3, 
        [data-testid="stSubheader"] span {{
            color: #ffff !important;
            font-size: 28px !important;
            font-weight: 700 !important;
        }}

        .block-container {{
            max-width: 600px;
            margin-top: 10vh;
        }}
        [data-testid="stVerticalBlockBorderWrapper"] > div:nth-child(1) {{
            background-color:#ffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
        [data-testid="stSubheader"] h2 {{
            color:#ffff !important;
        }}
        [data-testid="stWidgetLabel"] p {{
            color: #ffff !important;
        }}
        [data-testid="stPageLink"] {{
                color:#ffff
                
        }}

    </style>
    """,
    unsafe_allow_html=True
)

file_path = Path(__file__).parent / "users.json"


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
    st.markdown("""
            <style>
                div.stPageLink a {
                    color:#0000FF
                }
            </style>
        """, unsafe_allow_html=True)

st.page_link("pages/login.py",label = "Đăng nhập")