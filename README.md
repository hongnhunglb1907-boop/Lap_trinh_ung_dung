# LEND X
---
## Tác giả
* **Hồng Nhung** 

---

## Mục tiêu dự án
* **Định lượng rủi ro:** Chuyển đổi dữ liệu khách hàng thô thành điểm số tín dụng (Credit Score) thông qua các thuật toán học máy.
* **Minh bạch hóa mô hình (XAI):** Cung cấp cái nhìn chi tiết về lý do tại sao một hồ sơ bị từ chối hoặc chấp nhận thông qua trọng số của các biến đầu vào.
* **Tối ưu hóa tham số:** Xây dựng hệ thống cho phép thử nghiệm và tinh chỉnh các ngưỡng (threshold) phê duyệt linh hoạt.

---

## Chức năng trọng tâm của Engine
- **Dashboard tổng quan** — Thống kê hồ sơ, biểu đồ phân bố rủi ro, bộ lọc thời gian.
- **Danh sách hồ sơ** — Tìm kiếm realtime, gợi ý tự động, lọc và sắp xếp.
- **Kết quả chấm điểm** — Thang đo trực quan, mức rủi ro, thông tin khách hàng.
- **Phân tích chi tiết** — Giải thích từng yếu tố, tổng hợp cách tính điểm, khuyến nghị.


---

## Tech Stack & Algorithm

| Thành phần | Công nghệ |
|---|---|
| Backend | Python 3.12 · Django 4.2 |
| Frontend | HTML · Tailwind CSS · Lucide Icons |
| Database | SQLite |
---

## 🚀 Cài đặt và chạy

1. **Chuẩn bị dự án:** `git clone <repo-url>` và `cd dashboard_project`
2. **Cài đặt môi trường:** `pip install -r requirements.txt`
3. **Cấu trúc Database:** `python manage.py makemigrations dashboard` và `python manage.py migrate`
4. **Dữ liệu mẫu:** `python manage.py loaddata loan_profiles.json`
5. **Khởi động:** `python manage.py runserver`
