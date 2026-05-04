# 🤖 Trợ lý Tâm lý AI (AI Mood Tracker)
**Môn học:** Tư Duy Tính Toán - Bài thực hành số 2  
**Sinh viên thực hiện:** Tạ Quang Lân - 24120084

## 📌 Giới thiệu
Dự án là một ứng dụng Web tương tác, hoạt động như một trợ lý tâm lý ảo. Hệ thống sử dụng mô hình ngôn ngữ **PhoBERT** để phân tích cảm xúc (Tích cực, Tiêu cực, Trung tính) từ các câu chat tiếng Việt của người dùng. 

Hệ thống được thiết kế theo kiến trúc Client-Server tách biệt:
- **Frontend:** Xây dựng bằng `Streamlit`, cho phép người dùng đăng nhập và giao tiếp với AI.
- **Backend:** Xây dựng bằng `FastAPI`, xử lý logic AI và giao tiếp với Database.
- **Database & Auth:** Sử dụng `Firebase Authentication` để quản lý đăng nhập và `Firestore` để lưu trữ lịch sử trò chuyện.

---

## ⚙️ Hướng dẫn cài đặt môi trường

**Bước 1: Clone kho chứa này về máy**
```bash
git clone https://github.com/quanlan1501/TuDuyTinhToan_Lab2.git
cd TuDuyTinhToan_Lab2
```

**Bước 2: Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

**Bước 3: Cấu hình bảo mật**
Dự án yêu cầu file Private Key của Firebase để Backend có thể kết nối với Database. Bạn cần thêm file firebase_key.json vào bên trong thư mục backend/ trước khi khởi chạy hệ thống.

---

## 🚀 Hướng dẫn khởi chạy ứng dụng
Để ứng dụng hoạt động, cần chạy song song 2 Terminal cho Backend và Frontend.

**Bước 1: Khởi chạy Backend (FastAPI)**
Mở Terminal mới, di chuyển vào thư mục backend và chạy server:
```bash
cd backend
uvicorn main:app --reload
```

**Bước 2: Khởi chạy Frontend (Streamlit)**
Mở một Terminal khác, di chuyển vào thư mục frontend và chạy giao diện:
```bash
cd frontend
streamlit run app.py
```

### 🔑 Tài khoản Test
Để tiện cho việc chấm bài, thầy/cô có thể sử dụng tài khoản đã được cấu hình sẵn trên Firebase sau:
- **Email:** `test.lab2@gmail.com`
- **Mật khẩu:** `123456`

## 🎥 Video Demo
https://drive.google.com/drive/folders/1sz9FCR3-9OY7bP8LUPDUYtjZNcK-r8fC?usp=sharing


