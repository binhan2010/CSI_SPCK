
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Câu lạc bộ",
    page_icon="🏀",
    layout="wide"
)

BASE = Path(__file__).resolve().parents[1]
IMAGE_DIR = BASE / "image"
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f3f6fb, #e8f7f6, #fff2e8);
}
</style>
""", unsafe_allow_html=True)


st.title("🏀 Thông tin câu lạc bộ")

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
    st.header("Đơn đăng ký tham gia")
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

        submitted = st.form_submit_button("Gửi đơn đăng ký")

    if submitted:
        if not full_name.strip() or not email.strip() or "@" not in email:
            st.error("Vui lòng nhập họ tên và email hợp lệ.")
        else:
            st.success(
                f"Đã ghi nhận đơn đăng ký của {full_name} "
                f"vào câu lạc bộ {selected}!"
            )

st.markdown("---")
st.markdown(
    '<a href="/" target="_self">← Trang chủ</a>',
    unsafe_allow_html=True
)