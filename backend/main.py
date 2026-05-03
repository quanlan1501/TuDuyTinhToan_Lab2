from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import firebase_admin
from firebase_admin import credentials, firestore
import random
import datetime

app = FastAPI()

# 1. KẾT NỐI DATABASE BẰNG CHÌA KHÓA BÍ MẬT
print("Đang khởi động Database...")
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 2. KHỞI TẠO BỘ NÃO AI PHOBERT
print("Đang gọi AI PhoBERT về...")
classifier = pipeline("sentiment-analysis", model="wonrax/phobert-base-vietnamese-sentiment")

# Schema dữ liệu nhận từ Frontend
class ChatInput(BaseModel):
    user_id: str
    message: str

# 3. CÁC ENDPOINT THEO YÊU CẦU
@app.get("/")
def read_root():
    return {"status": "AI Mood Backend đang chạy ngon lành!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# 4. ENDPOINT CHÍNH: XỬ LÝ CHAT, PHÂN TÍCH VÀ LƯU DATABASE
@app.post("/chat")
def chat_with_ai(data: ChatInput):
    if not data.message.strip():
        raise HTTPException(status_code=400, detail="Chưa nhập gì kìa ní!")

    # A. Nhờ AI đọc cảm xúc
    result = classifier(data.message)[0]
    sentiment = result["label"]

    # B. Xử lý "Smart Response" (Phản hồi thông minh - Bản nâng cấp EQ)
    text_lower = data.message.lower()
    
    # Nhóm 1: Tình cảm / Mối quan hệ 💔❤️
    if any(word in text_lower for word in ["chia tay", "người yêu", "thất tình", "crush", "cô đơn", "cãi nhau"]):
        if sentiment == "NEG":
            response_text = "Buồn nào rồi cũng sẽ qua thôi. Khóc một trận thật to, ăn một món thật ngon rồi ngủ một giấc nhé. Bạn xứng đáng với những điều tốt đẹp hơn!"
        else:
            response_text = "Chuyện tình cảm có vẻ đang mang lại nhiều cảm xúc cho bạn nhỉ? Hãy cứ tận hưởng những khoảnh khắc này nhé!"
            
    # Nhóm 2: Học tập / Deadline / Code 💻📚
    elif any(word in text_lower for word in ["thi", "deadline", "báo cáo", "code", "bug", "đồ án", "rớt môn", "gpa"]):
        if sentiment == "NEG":
            response_text = "Chạy deadline hay fix bug mệt mỏi quá đúng không? Gấp máy lại, làm tách cà phê hoặc dạo vài vòng Los Santos rồi quay lại chiến đấu tiếp nhé. Sắp qua môn rồi!"
        else:
            response_text = "Phong độ code đang lên cao đúng không? Giữ vững tinh thần này để húp trọn điểm A+ môn này nhé!"
            
    # Nhóm 3: Sức khỏe / Thể chất 🏋️‍♂️🛌
    elif any(word in text_lower for word in ["mệt", "đau", "bệnh", "đói", "buồn ngủ", "đuối", "tạ", "gym"]):
        response_text = "Sức khỏe là quan trọng nhất! Cơ thể đang đình công rồi đấy. Nhớ ăn uống đầy đủ, nghỉ ngơi phục hồi cơ bắp rồi hãy làm tiếp nha."
        
    # Nhóm 4: Phản hồi chung chung (Nếu không trúng từ khóa nào)
    elif sentiment == "POS":
        responses = [
            "Năng lượng tích cực quá! Giữ vững phong độ nhé!",
            "Tuyệt vời! Nghe bạn vui làm mình cũng vui lây.",
            "10 điểm không có nhưng! Chúc bạn ngày mai cũng vui như thế này."
        ]
        response_text = random.choice(responses)
    elif sentiment == "NEG":
        responses = [
            "Cuộc sống đôi khi hơi áp lực một chút. Bạn đã làm rất tốt rồi, cho phép bản thân nghỉ ngơi một lát nhé.",
            "Mọi chuyện rồi sẽ ổn thôi. Mai là một ngày mới đầy hy vọng mà!",
            "Đừng ôm hết buồn bực vào người. Hít thở sâu và thư giãn đi bạn nhé."
        ]
        response_text = random.choice(responses)
    else:  # NEU (Trung tính)
        response_text = "Một ngày bình yên ha. Cứ thong thả mà lập kế hoạch cho ngày mai nhé."

    # C. Lưu toàn bộ xuống Firestore Database
    doc_data = {
        "user_id": data.user_id,
        "message": data.message,
        "sentiment": sentiment,
        "response": response_text,
        "timestamp": datetime.datetime.now().isoformat()
    }
    db.collection("chat_history").add(doc_data)

    return doc_data

# 5. ENDPOINT LẤY LỊCH SỬ CHAT THEO USER [cite: 93]
@app.get("/messages")
def get_messages(user_id: str):
    # Kéo dữ liệu từ Firebase về dựa theo đúng user_id [cite: 83]
    docs = db.collection("chat_history").where("user_id", "==", user_id).stream()
    
    history = []
    for doc in docs:
        history.append(doc.to_dict())
    
    # Sắp xếp lại theo thời gian thực tế
    history = sorted(history, key=lambda x: x["timestamp"])
    
    return {"history": history}