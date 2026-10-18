import streamlit as st
import base64
import json
import re
import hashlib
from pathlib import Path

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
#         .stApp {{
#             background: transparent !important;
#         }}
#         .stApp::before {{
#             content: "";
#             position: fixed;
#             top: 0;
#             left: 0;
#             width: 100%;
#             height: 100%;
#             background-image: url("data:image/png;base64,{image}");
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#             z-index: -2;
#         }}
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

                            salt = user.get("salt")
                            password_hash = user.get("password_hash")

                            if (
                                user.get("username") == username
                                and salt
                                and password_hash
                            ):
                                hashed = hashlib.pbkdf2_hmac(
                                    "sha256",
                                    password.encode("utf-8"),
                                    salt.encode("utf-8"),
                                    600000
                                ).hex()

                                if hashed == password_hash:
                                    found = True
                                    break

                        if found:
                            st.success("🎉 Đăng nhập thành công!")
                        else:
                            st.error(
                                "Username hoặc mật khẩu không chính xác."
                            )

                except (json.JSONDecodeError, OSError):
                    st.error(
                        "Không thể đọc dữ liệu tài khoản. "
                        "Hãy kiểm tra file users.json."
                    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <style>
            div.stPageLink a {
                color:#0000FF
                
            }
        </style>
    """, unsafe_allow_html=True)
st.page_link("pages/register.py", label="Đăng ký")
st.page_link("home.py",label="Trang chủ")
