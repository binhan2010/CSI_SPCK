
import streamlit as st
import base64
from pathlib import Path
st.set_page_config(
    page_title="BasketZone",
    layout="wide",
    initial_sidebar_state="collapsed"
)


BASE_DIR = Path(__file__).parent
BG_PATH = BASE_DIR / "image" / "bg.jpg"

if BG_PATH.exists():
    bg = base64.b64encode(BG_PATH.read_bytes()).decode()
else:
    bg = ""

st.markdown(f"""
<style>
.stApp {{
    background:
        linear-gradient(rgba(10, 20, 40, 0.65),
                        rgba(10, 20, 40, 0.65)),
        url("data:image/jpeg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

[data-testid="stSidebar"] {{
    display: none;
}}

.block-container {{
    max-width: 1200px;
    padding-top: 12vh;
}}


.stPageLink a,
.stPageLink a:hover,
.stPageLink a:active,
.stPageLink a:focus {{
    background-color: white !important;
    color: #333333 !important;
    border: 1px solid white !important;
    border-radius: 8px;
    padding: 12px;
    justify-content: center;
    box-shadow: none !important;
    text-decoration: none !important;
}}



.brand {{
    color: white;
    font-size: 65px;
    font-weight: bold;
    margin-left: 15%;
}}


.intro {{
    color: white;
    font-size: 20px;
    line-height: 1.7;
    margin: 20px 0 50px 15%;
}}


.stPageLink a {{
    background-color: white;
    color: #333333 !important;
    border: 1px solid white;
    border-radius: 8px;
    padding: 10px;
    justify-content: center;
}}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="brand">BasketZone</div>

<div class="intro">
    Khám phá các câu lạc bộ bóng rổ nổi tiếng cập nhật thông tin, tham gia cộng đồng và trải nghiệm thế giới bóng rổ ngay hôm nay!
</div>
""", unsafe_allow_html=True)


left, center, right = st.columns([1,4,1])

with center:
    col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.page_link(
    #         "pages/club.py",
    #         label="Khám phá câu lạc bộ",
    #         use_container_width=True
    #     )

    with col2:
        st.page_link(
            "pages/login.py",
            label="Đăng nhập",
            use_container_width=True
        )

    # with col3:
    #     st.page_link(
    #         "pages/login.py",
    #         label="Đăng nhập",
    #         use_container_width=True
    #     )
st.markdown("""
<div style="
    text-align: center;
    color: #cccccc;
    margin-top: 100px;
    font-size: 12px;
    letter-spacing: 3px;">
    BASKETZONE
</div>
""", unsafe_allow_html=True)




# import streamlit as st
# import base64
# from pathlib import Path

# st.set_page_config(page_title="BasketZone", page_icon="🏀", layout="wide",
#                    initial_sidebar_state="collapsed")

# BASE_DIR = Path(__file__).resolve().parent
# IMAGE_DIR = BASE_DIR / "image"
# BG_PATH = IMAGE_DIR / "bg.jpg"

# def background_css(path, overlay="rgba(10, 20, 40, 0.65)"):
#     if path.is_file():
#         encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
#         mime = "image/jpeg" if path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
#         image_css = f'url("data:{mime};base64,{encoded}")'
#     else:
#         image_css = "none"
#     st.markdown(f"""
#     <style>
#     [data-testid="stSidebar"] {{display:none;}}
#     .stApp {{
#         background-image: linear-gradient({overlay}, {overlay}), {image_css};
#         background-size: cover;
#         background-position: center;
#         background-attachment: fixed;
#     }}
#     .block-container {{max-width: 1200px; padding-top: 10vh;}}
#     .brand {{color:white; font-size: clamp(42px, 6vw, 68px); font-weight:800;
#              margin-left: 5%;}}
#     .intro {{color:white; font-size:20px; line-height:1.7;
#              margin: 18px 5% 42px; max-width:850px;}}
#     div.stPageLink a {{
#         background: white !important; color:#222 !important;
#         border:1px solid white !important; border-radius:10px !important;
#         min-height:48px; justify-content:center; font-weight:600;
#     }}
#     div.stPageLink a * {{color:#222 !important;}}
#     </style>
#     """, unsafe_allow_html=True)

# background_css(BG_PATH)
# st.markdown("""
# <div class="brand">BasketZone</div>
# <div class="intro">
# Khám phá các câu lạc bộ bóng rổ, cập nhật thông tin, tham gia cộng đồng
# và trải nghiệm thế giới bóng rổ ngay hôm nay!
# </div>
# """, unsafe_allow_html=True)

# _, center, _ = st.columns([1, 5, 1])
# with center:
#     c1, c2, c3 = st.columns(3)
#     with c1:
#         st.page_link("pages/club.py", label="🏀 Khám phá câu lạc bộ", use_container_width=True)
#     with c2:
#         st.page_link("pages/chatbot.py", label="💬 Chatbot", use_container_width=True)
#     with c3:
#         st.page_link("pages/login.py", label="👤 Đăng nhập", use_container_width=True)

# st.markdown("""
# <div style="text-align:center;color:#ddd;margin-top:100px;font-size:12px;letter-spacing:3px;">
# BASKETZONE
# </div>
# """, unsafe_allow_html=True)
