#%% LIB
from __future__ import annotations
import streamlit as st


#%% PAGE CONFIG

st.markdown("""
            # 🧰 Thư viện Công cụ hữu ích
            
            Danh sách các công cụ/nguồn tài nguyên giúp thầy cô làm việc hiệu quả với GenAI, soạn bài, tạo câu hỏi, quản lý lớp học, v.v.
            
            ---
            
            """)


# Danh sách link
st.markdown("""
- [MassiveMark Playground](https://www.bibcit.com/vi/massivemark) - Chuyển text từ GenAI thành văn bản Word (hỗ trợ định dạng công thức toán học)
- [Perplexity AI](https://www.perplexity.ai/) – Công cụ tìm kiếm AI có trích dẫn nguồn (miễn phí tính năng Search cơ bản, đảm bảo thông tin kiến thức cập nhật)
- [Suno AI](https://suno.com/) - Cho phép tạo vài bản nhạc mỗi ngày bằng AI, thích hợp cho các hoạt động khởi động của lớp học.
- [Canva for Education](https://www.canva.com/education/) – Thiết kế slide và tài liệu giảng dạy
""")

st.markdown("---")

st.markdown("""
            Bạn có thể đề xuất thêm công cụ hữu ích để tôi cập nhật vào danh sách này.
            
       <a href="https://docs.google.com/forms/d/e/1FAIpQLSe9OaT78-54AvhkNRPENMsuGLv4WytUVNau78d_luR2xFdc8g/viewform?usp=dialog" target="_blank">
           <button style="padding:0.6rem 1rem; border-radius:8px; margin-bottom: 20px">
               ĐỀ XUẤT CÔNG CỤ NGAY ↗
           </button>
       </a>
       
            """, unsafe_allow_html=True)
