import streamlit as st
import json
from pathlib import Path
from datetime import date

st.set_page_config(page_title="Đặt sân", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

# CSS giao diện
st.markdown("""
<style>
#MainMenu, footer, header {
    visibility: hidden;
}
[data-testid="stSidebar"] {
    display: none;
}
.block-container {
    padding-top: 5rem;padding-bottom: 2rem;max-width: 1200px;
}
.stApp {
    background: white;color: #222;
}
.navbar {
    position: fixed;top: 0;left: 0;width: 100%;height: 75px;box-sizing: border-box;
    display: flex;justify-content: space-between;align-items: center;background: rgba(15, 15, 15, 0.96);border-bottom: 1px solid #333;
    padding: 0 40px;
    z-index: 9999;
}
.logo {
    color: #ff861f;font-size: 25px;font-weight: 800;
}
.nav-links {
    display: flex;gap: 22px;flex-wrap: wrap;
}
.nav-links a {
    color: white;text-decoration: none;font-weight: 600;font-size: 14px;
}
.nav-links a:hover {
    color: #ff861f;
}

div.stButton > button {
    border-radius: 10px;min-height: 43px;font-weight: 700;
}
div.stButton > button[kind="primary"] {
    background: #ff861f !important;color: #222 !important;border: 1px solid #ff861f !important;
}
div.stButton > button[kind="secondary"],
div.stButton > button[kind="primary"] {
    background-color: #ff861f !important;color: #111111 !important;border: 1px solid #ff861f !important;border-radius: 10px;font-weight: 700;margin-top:15px
}

/* Không đổi màu khi hover */
div.stButton > button[kind="secondary"]:hover,
div.stButton > button[kind="primary"]:hover {
    background-color: #ff861f !important;
    color: #111111 !important;
    border: 1px solid #ff861f !important;
}
/* Giờ chưa chọn: màu trắng */
div.stButton > button[kind="secondary"] {
    background: white !important;
    color: #222 !important;
    border: 1px solid #ddd !important;
}

/* Không đổi màu khi hover */
div.stButton > button[kind="primary"]:hover {
    background: #ff861f !important;
    color: #222 !important;
}

div.stButton > button[kind="secondary"]:hover {
    background: white !important;
    color: #222 !important;
}

div.stButton > button:disabled {
    background: #cccccc !important;
    color: #666666 !important;
    border: 1px solid #cccccc !important;
}

div[data-testid="stTextInput"] input {
    background: white;
    color: black;
    border: 1px solid #ddd;
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: #999;
    margin-top: 35px;
    padding: 20px;
    border-top: 1px solid #eee;
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
courts = {
    "Sân Hà Đông": {"address":"Hà Đông, Hà Nội", "price":200000, "description":"Phù hợp cho các buổi tập và thi đấu."},
    "Sân Cầu Giấy": {"address":"Cầu Giấy, Hà Nội", "price":250000, "description":"Không gian cho những trận bóng sôi động."},
    "Sân Thanh Xuân": {"address":"Thanh Xuân, Hà Nội", "price":180000, "description":"Lựa chọn tiết kiệm để chơi bóng."},
    "Sân Phòng Không Không Quân": {"address":"108 Lê Trọng Tấn, Thanh Xuân, Hà Nội", "price":600000, "description":"Cụm sân bóng rổ phục vụ tập luyện và thi đấu."},
    "Sân bóng rổ 3PTS": {"address":"2 Cổ Linh, Long Biên, Hà Nội", "price":300000, "description":"Sân trong nhà, có điều hòa."},
    "Sân bóng rổ Văn Quán": {"address":"Khu đô thị Văn Quán, Hà Đông, Hà Nội", "price":200000, "description":"Sân bóng rổ ngoài trời dành cho cộng đồng."},
    "Sân The Puzzle": {"address":"Ngõ 12 Núi Trúc, Ba Đình, Hà Nội", "price":250000, "description":"Địa điểm chơi bóng rổ và giao lưu."},
    "Sân bóng rổ Bách Khoa": {"address":"Khu vực Lê Thanh Nghị, Hai Bà Trưng, Hà Nội", "price":200000, "description":"Sân bóng rổ ngoài trời trong khu vực Đại học Bách Khoa."},
    "Sân bóng rổ Lương Thế Vinh": {"address":"55 Đinh Núp, Cầu Giấy, Hà Nội", "price":250000, "description":"Sân tập luyện bóng rổ trong khu vực Nam Trung Yên."},
    "Sân bóng rổ Hồ Đền Lừ": {"address":"Khu vực hồ Đền Lừ, Hoàng Mai, Hà Nội", "price":180000, "description":"Sân bóng rổ ngoài trời, không gian thoáng."},
    "Sân bóng rổ Firesport": {"address":"55 Đốc Ngữ, Ba Đình, Hà Nội", "price":250000, "description":"Địa điểm tập luyện bóng rổ."},
    "Sân bóng rổ Junsport": {"address":"489 Hoàng Quốc Việt, Cầu Giấy, Hà Nội", "price":250000, "description":"Không gian tập luyện bóng rổ trong nhà."},
    "Sân bóng rổ Fire Sport The New Quarter": {"address":"612 Hoàng Hoa Thám, Hà Nội", "price":250000, "description":"Sân chơi dành cho cộng đồng yêu bóng rổ."}
}

file_json_path = Path(__file__).parent / "booking.json"

def load_bookings():
    try:
        with open(file_json_path, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

def save_bookings(data):
    with open(file_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Tk
st.title("Đặt lịch sân bóng rổ")
tim = st.text_input("Tìm kiếm sân", placeholder="Nhập tên sân hoặc khu vực")
query = tim.strip().lower()

ket_qua = [ten for ten, tt in courts.items()
           if query and (query in ten.lower() or query in tt["address"].lower())]

for ten in ket_qua:
    tt = courts[ten]
    with st.container(border=True):
        st.subheader(ten)
        st.write(tt["address"])
        st.caption(tt["description"])
        st.write(f"**{tt['price']:,} VNĐ/giờ**")

        if st.button("Chọn sân", key=f"chon_{ten}", type="primary"):
            st.session_state["san_chon"] = ten
            st.rerun()

if query and not ket_qua:
    st.warning("Không tìm thấy sân phù hợp.")


# chọn sân
san = st.session_state.get("san_chon")

if san in courts:
    tt = courts[san]
    st.divider()
    st.header(f"Đặt lịch: {san}")
    st.write(tt["address"])

    ngay = st.date_input("Ngày thuê", min_value=date.today(), key=f"ngay_{san}")
    cac_gio = list(range(7, 21, 2))
    ma_gio = f"gio_{san}_{ngay}"
    lich = load_bookings()

    # grid
    for hang in range(0, len(cac_gio), 4):
        cot = st.columns(4)

        for j, gio in enumerate(cac_gio[hang:hang+4]):
            trung = any(
                b["court"] == san and b["date"] == str(ngay)
                and gio < b["start"] + b["hours"]
                and b["start"] < gio + 2
                for b in lich
            )

            chon = st.session_state.get(ma_gio) == gio

            with cot[j]:
                if st.button(
                    f"{gio:02d}:00 - {gio+2:02d}:00",
                    key=f"{ma_gio}_{gio}",
                    disabled=trung,
                    type="primary" if chon else "secondary",
                    use_container_width=True
                ):
                    st.session_state[ma_gio] = gio
                    st.rerun()

    # TT
    gio_chon = st.session_state.get(ma_gio)
    so_gio = 2
    tong_tien = tt["price"] * so_gio

    ho_ten = st.text_input("Họ và tên", key="ho_ten")
    sdt = st.text_input("Số điện thoại", key="sdt")

    st.markdown(f"""
    <div style="background:#fff0e2;padding:18px;border-radius:12px;">
        <div>Tổng chi phí</div>
        <div style="font-size:26px;font-weight:bold;color:#ed7815;">
            {tong_tien:,} VNĐ
        </div>
        Giá thuê: {tt['price']:,} VNĐ/giờ × {so_gio} giờ
    </div>
    """, unsafe_allow_html=True)

    if st.button("Xác nhận đặt sân", type="primary"):
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
                b["court"] == san and b["date"] == str(ngay)
                and gio_chon < b["start"] + b["hours"]
                and b["start"] < gio_chon + so_gio
                for b in lich
            )

            if trung:
                st.error("Khung giờ này đã có người đặt.")
            else:
                lich.append({
                    "court":san, "address":tt["address"],
                    "name":ho_ten.strip(), "phone":sdt_sach,
                    "date":str(ngay), "start":gio_chon,
                    "hours":so_gio, "price":tong_tien
                })

                try:
                    save_bookings(lich)
                    st.session_state.pop("san_chon", None)
                    st.session_state.pop(ma_gio, None)
                    st.success("Đặt sân thành công!")
                    st.rerun()
                except OSError:
                    st.error("Không thể lưu lịch đặt sân.")

st.divider()
st.header("Lịch đã đặt sân")
bookings = load_bookings()

if bookings:
    for i, b in enumerate(bookings):
        with st.container(border=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                st.subheader(b["court"])
                st.write(b["address"])
                st.write("Người đặt:", b["name"])
                st.write("Ngày chơi:", b["date"])
                st.write(f"{b['start']:02d}:00 - {b['start']+b['hours']:02d}:00")
                st.write(f"**{b['price']:,} VNĐ**")

            with col2:
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
