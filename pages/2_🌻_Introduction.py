import streamlit as st

st.markdown("""
            # 🌻 Giới thiệu về GenAI
            
            Giúp các thầy cô hiểu hơn về GenAI.
            
            ---
            
            """)

st.image(
    "pages/materials/gen-ai-image.png",
    width=300
    )

st.markdown("""
### GenAI là gì?
GenAI (Generative AI – Trí tuệ nhân tạo sinh sinh) là công nghệ có khả năng tạo ra nội dung mới như văn bản, hình ảnh, âm nhạc hoặc bài giảng dựa trên dữ liệu đã được huấn luyện. 
Thay vì chỉ đưa ra câu trả lời có/không, GenAI có thể sáng tạo, mô phỏng phong cách viết, và đưa ra gợi ý phù hợp với ngữ cảnh.

### GenAI hoạt động như thế nào?
Các mô hình GenAI, như ChatGPT, được huấn luyện trên một lượng dữ liệu khổng lồ. Chúng học cách dự đoán từ tiếp theo trong một câu, và từ đó tạo thành văn bản mạch lạc. 
Trong giáo dục, GenAI có thể đóng vai trò như một “trợ giảng ảo”, giúp giáo viên xây dựng kế hoạch bài dạy, thiết kế câu hỏi, hay tạo ra tài liệu tham khảo nhanh chóng.

### Tại sao prompt lại quan trọng?
Prompt chính là “câu lệnh” mà giáo viên gửi tới GenAI. Một prompt càng rõ ràng, cụ thể thì kết quả nhận được càng sát với nhu cầu. 
Nếu prompt mơ hồ, câu trả lời sẽ chung chung hoặc không hữu ích. Vì vậy, việc viết một prompt đúng, đủ thông tin (bối cảnh, nhiệm vụ, dữ liệu, kết quả mong đợi) sẽ giúp GenAI hiểu đúng mục tiêu và tạo ra nội dung chất lượng.
""")
