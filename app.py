import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cau hinh trang web
st.set_page_config(page_title="Quản lý điểm sinh viên", layout="wide")

# Tao du lieu 10 sinh vien
data = {
    "Họ tên": [
        "Nguyễn Văn An",
        "Nguyễn Nhật Phong",
        "Trần Nguyễn Trúc Ly",
        "Ngô Thị Nga",
        "Nguyễn Kim Anh",
        "Đặng Văn Minh",
        "Nguyễn Thị Yến Nhi",
        "Phạm Hữu Sang",
        "Trần Minh Thư",
        "Cao Tấn Phát"
    ],
    "Chuyên cần": [8, 9, 7, 8, 6, 9, 8, 7, 6, 8],
    "Giữa kỳ": [8, 8, 7, 9, 6, 5, 7, 9, 5, 9],
    "Cuối kỳ": [7, 6, 9, 8, 7, 9, 6, 8, 6, 9]
}

# Tao bang du lieu
df = pd.DataFrame(data)

# Tinh diem tong ket
df["Tổng kết"] = (
    0.2 * df["Chuyên cần"]
    + 0.3 * df["Giữa kỳ"]
    + 0.5 * df["Cuối kỳ"]
)

# Xep loai sinh vien
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# Tieu de
st.title("QUẢN LÝ ĐIỂM SINH VIÊN-")

# Hien thi bang diem
st.subheader("1. Bảng điểm sinh viên")
bang_diem = df.copy()
bang_diem["Tổng kết"] = bang_diem["Tổng kết"].round(2)
st.dataframe(bang_diem, use_container_width=True, hide_index=True)

# Thong ke
st.subheader("2. Thống kê của lớp")
diem_trung_binh = df["Tổng kết"].mean()
diem_cao_nhat = df["Tổng kết"].max()
diem_thap_nhat = df["Tổng kết"].min()
so_sinh_vien_dat = (df["Tổng kết"] >= 5).sum()

cot1, cot2, cot3, cot4 = st.columns(4)
cot1.metric("Điểm trung bình lớp", f"{diem_trung_binh:.2f}")
cot2.metric("Điểm cao nhất", f"{diem_cao_nhat:.2f}")
cot3.metric("Điểm thấp nhất", f"{diem_thap_nhat:.2f}")
cot4.metric("Số sinh viên đạt (>= 5)", int(so_sinh_vien_dat))

st.write("**Sinh viên có điểm cao nhất:**")
st.dataframe(df[df["Tổng kết"] == diem_cao_nhat][["Họ tên", "Tổng kết", "Xếp loại"]],
             use_container_width=True, hide_index=True)

st.write("**Sinh viên có điểm thấp nhất:**")
st.dataframe(df[df["Tổng kết"] == diem_thap_nhat][["Họ tên", "Tổng kết", "Xếp loại"]],
             use_container_width=True, hide_index=True)

# Chon sinh vien
st.subheader("3. Xem điểm từng sinh viên")
ten_sinh_vien = st.selectbox("Chọn một sinh viên:", df["Họ tên"])
sinh_vien = df[df["Họ tên"] == ten_sinh_vien].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", f'{sinh_vien["Chuyên cần"]:.1f}')
c2.metric("Giữa kỳ", f'{sinh_vien["Giữa kỳ"]:.1f}')
c3.metric("Cuối kỳ", f'{sinh_vien["Cuối kỳ"]:.1f}')
c4.metric("Tổng kết", f'{sinh_vien["Tổng kết"]:.2f}')
c5.metric("Xếp loại", sinh_vien["Xếp loại"])

# Bieu do cot
st.subheader("4. Biểu đồ điểm tổng kết")
fig, ax = plt.subplots()
ax.bar(df["Họ tên"], df["Tổng kết"])
ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Chan trang: thay thong tin bang thong tin cua ban
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size:12px; color:gray;'>"
    "Người tạo ứng dụng: [Nhập họ tên của bạn] | MSSV: [Nhập MSSV của bạn]"
    "</div>",
    unsafe_allow_html=True
)
