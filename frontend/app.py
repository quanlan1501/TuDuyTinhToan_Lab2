import streamlit as st
import requests

# CẤU HÌNH KẾT NỐI
BACKEND_URL = "http://127.0.0.1:8000"
# Dán API Key Firebase của bạn vào dấu ngoặc kép bên dưới:
FIREBASE_API_KEY = "AIzaSyAi6-LTkJBZEB7IDeRdSrVlu9tnPR4g0oQ" 

st.set_page_config(page_title="AI Mood Tracker", page_icon="🤖")

# HÀM XỬ LÝ ĐĂNG NHẬP (Dùng Firebase REST API)
def login_firebase(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    return r.json()

# QUẢN LÝ TRẠNG THÁI ĐĂNG NHẬP
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ==========================================
# MÀN HÌNH 1: ĐĂNG NHẬP
# ==========================================
if not st.session_state.user_id:
    st.title("🔐 Đăng nhập hệ thống")
    st.write("Vui lòng đăng nhập bằng tài khoản Firebase để sử dụng Trợ lý Tâm lý AI.")
    
    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")
    
    if st.button("Đăng nhập"):
        if email and password:
            res = login_firebase(email, password)
            if "localId" in res:
                st.session_state.user_id = res["localId"]  # Lưu ID người dùng
                st.session_state.email = email
                st.success("Đăng nhập thành công! Đang vào ứng dụng...")
                st.rerun()
            else:
                st.error("Sai email hoặc mật khẩu, hoặc tài khoản chưa được tạo trên Firebase.")
        else:
            st.warning("Vui lòng nhập đủ thông tin!")

# ==========================================
# MÀN HÌNH 2: GIAO DIỆN CHATBOT CHÍNH
# ==========================================
else:
    st.title(f"🤖 Trợ lý Tâm lý AI")
    st.caption(f"Đang đăng nhập với: {st.session_state.email}")
    
    if st.button("Đăng xuất"):
        st.session_state.user_id = None
        st.rerun()
        
    st.divider()

    # 1. HIỂN THỊ LỊCH SỬ CHAT TỪ DATABASE
    st.subheader("Lịch sử trò chuyện của bạn")
    try:
        res = requests.get(f"{BACKEND_URL}/messages?user_id={st.session_state.user_id}")
        if res.status_code == 200:
            history = res.json().get("history", [])
            for item in history:
                # Icon cảm xúc
                icon = "🟢" if item['sentiment'] == "POS" else "🔴" if item['sentiment'] == "NEG" else "⚪"
                
                # Khung chat của user
                with st.chat_message("user"):
                    st.write(item["message"])
                # Khung chat của AI
                with st.chat_message("assistant"):
                    st.write(f"**Cảm xúc nhận diện:** {icon} {item['sentiment']}")
                    st.write(item["response"])
        else:
            st.error("Không thể kết nối đến Backend để lấy lịch sử.")
    except Exception as e:
        st.warning("Đang chờ Backend khởi động...")

    st.divider()

    # 2. KHU VỰC NHẬP TIN NHẮN MỚI
    user_input = st.chat_input("Hôm nay bạn cảm thấy thế nào? Hãy kể cho mình nghe...")
    
    if user_input:
        # Gửi dữ liệu xuống Backend
        payload = {"user_id": st.session_state.user_id, "message": user_input}
        try:
            with st.spinner("AI đang suy nghĩ..."):
                post_res = requests.post(f"{BACKEND_URL}/chat", json=payload)
                
            if post_res.status_code == 200:
                st.rerun() # Load lại trang để hiện tin nhắn mới
            else:
                st.error("Có lỗi xảy ra khi xử lý tin nhắn.")
        except Exception as e:
            st.error(f"Lỗi kết nối Backend: {e}")