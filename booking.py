import streamlit as st
import json
from pathlib import Path
from datetime import date
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
    background:#ffff;
    color:black;
    border: 1px ;
    border-radius: 10px;
}

.answer-box {
    background: #ffff;
    border-left: 4px solid;
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

st.set_page_config(
    page_title="Đặt sân",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

courts = {
    "Sân Hà Đông": {
        "address": "Hà Đông, Hà Nội",
        "price": 200000,
        "description": "Phù hợp cho các buổi tập và thi đấu."
    },
    "Sân Cầu Giấy": {
        "address": "Cầu Giấy, Hà Nội",
        "price": 250000,
        "description": "Không gian cho những trận bóng sôi động."
    },
    "Sân Thanh Xuân": {
        "address": "Thanh Xuân, Hà Nội",
        "price": 180000,
        "description": "Lựa chọn tiết kiệm để chơi bóng."
    }
}

file_json_path = Path(__file__).parent / "booking.json"


def load_bookings():
    if file_json_path.exists():
        try:
            with open(file_json_path, encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_bookings(data):
    with open(file_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Tìm kiếm sân
st.title("Đặt lịch sân bóng rổ")
tim = st.text_input("Tìm kiếm sân", placeholder="Nhập tên sân hoặc khu vực")

ket_qua = [
    ten for ten, tt in courts.items()
    if tim.strip().lower() in ten.lower()
    or tim.strip().lower() in tt["address"].lower()
] if tim.strip() else []

for ten in ket_qua:
    tt = courts[ten]

    with st.container(border=True):
        st.subheader(ten)
        st.write(tt["address"])
        st.caption(tt["description"])
        st.markdown(
            f"<div class='price'>{tt['price']:,} VNĐ/giờ</div>",
            unsafe_allow_html=True
        )

        if st.button("Chọn sân", key=f"chon_{ten}"):
            st.session_state["san_chon"] = ten
            st.rerun()

if tim.strip() and not ket_qua:
    st.warning("Không tìm thấy sân phù hợp.")

# Đặt sân
san = st.session_state.get("san_chon")

if san in courts:
    tt = courts[san]
    st.divider()
    st.header(f"Đặt lịch: {san}")
    st.write(tt["address"])

    ngay = st.date_input("Ngày thuê", min_value=date.today())
    cac_gio = list(range(7, 21, 2))
    ma_gio = f"gio_{san}_{ngay}"

    #grid
    for hang in range(0, len(cac_gio), 4):
        cot = st.columns(4)

        for j, gio in enumerate(cac_gio[hang:hang + 4]):
            lich = load_bookings()

            bi_trung = any(
                b["court"] == san
                and b["date"] == str(ngay)
                and gio < b["start"] + b["hours"]
                and b["start"] < gio + 2
                for b in lich
            )

            dang_chon = st.session_state.get(ma_gio) == gio

            mau ="#cccccc" if bi_trung else (
            "#ff861f" if dang_chon else "#ffffff"
            )

            with cot[j]:
                st.markdown(
                    f"""
                    <style>
                    div.st-key-{ma_gio}_{gio} button {{
                        background: {mau};
                        color: #222;
                        border: 1px solid #ddd;
                    }}
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"{gio:02d}:00 - {gio+2:02d}:00",
                    key=f"{ma_gio}_{gio}",
                    disabled=bi_trung
                ):
                    st.session_state[ma_gio] = gio
                    st.rerun()

    gio_chon = st.session_state.get(ma_gio)
    so_gio = 2
    tong_tien = tt["price"] * so_gio

    ho_ten = st.text_input("Họ và tên", key="ho_ten")
    sdt = st.text_input("Số điện thoại", key="sdt")

    st.markdown(f"""
    <div style="background:#fff0e2; padding:18px; border-radius:12px;">
        <div>Tổng chi phí</div>
        <div style="font-size:26px;font-weight:bold;color:#ed7815;">
            {tong_tien:,} VNĐ
        </div>
        {tt['price']:,} đ
    </div>
    """, unsafe_allow_html=True)

    if st.button("Xác nhận đặt sân"):
        sdt_sach = sdt.strip().replace(" ", "")

        if not ho_ten.strip() or not sdt_sach:
            st.error("Vui lòng nhập họ tên và số điện thoại.")
        elif not sdt_sach.isdigit() or len(sdt_sach) < 9:
            st.error("Số điện thoại cần ít nhất 9 chữ số.")
        elif gio_chon not in cac_gio:
            st.error("Vui lòng chọn khung giờ.")
        else:
            lich = load_bookings()

            trung = any(
                b["court"] == san
                and b["date"] == str(ngay)
                and gio_chon < b["start"] + b["hours"]
                and b["start"] < gio_chon + so_gio
                for b in lich
            )

            if trung:
                st.error("Khung giờ này đã có người đặt.")
            else:
                lich.append({
                    "court": san,
                    "address": tt["address"],
                    "name": ho_ten.strip(),
                    "phone": sdt_sach,
                    "date": str(ngay),
                    "start": gio_chon,
                    "hours": so_gio,
                    "price": tong_tien
                })

                try:
                    save_bookings(lich)
                    st.session_state.pop("san_chon", None)
                    st.session_state.pop(ma_gio, None)
                    st.success("Đặt sân thành công!")
                    st.rerun()
                except OSError:
                    st.error("Không thể lưu lịch đặt sân.")

#hiện file lịch đã đặt
st.divider()
st.header("Lịch đã đặt sân")

bookings = load_bookings()

if bookings:
    for i, b in enumerate(bookings):
        with st.container(border=True):
            cot1, cot2 = st.columns([4, 1])

            with cot1:
                st.subheader(b["court"])
                st.write(b["address"])
                st.write("Người đặt:", b["name"])
                st.write("Ngày chơi:", b["date"])
                st.write(
                    f"{b['start']:02d}:00 - "
                    f"{b['start'] + b['hours']:02d}:00"
                )
                st.write(f"**{b['price']:,} VNĐ**")

            with cot2:
                if st.button("Hủy lịch", key=f"huy_{i}"):
                    bookings.pop(i)
                    save_bookings(bookings)
                    st.rerun()
else:
    st.info("Chưa có lịch đặt sân nào.")

st.markdown("""
<div class="footer">
    <b>BasketZone</b><br>
    Kết nối đam mê bóng rổ của bạn.
</div>
""", unsafe_allow_html=True)




